"""FastAPI route handlers for local statement ingestion and status querying.

Guarantees:
- Zero PII egress in API responses and structured logs.
- Strict contract enforcement: fails loudly on invalid payloads or schemas.
- Complete round-trip extraction and canonical persistence across all domains.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from app.adapters.registry import get_default_registry
from app.api.schemas import (
    AccountSummaryResponse,
    ExtractionRunDetailResponse,
    HealthResponse,
    IngestErrorResponse,
    IngestSuccessResponse,
)
from app.db.connection import get_db_connection
from app.db.repository import get_extraction_run, get_run_statements
from app.models.enums import (
    AccountDomain,
    AccountType,
    CurrencyCode,
    RunStatus,
)
from app.pipeline.ingest_service import IngestFailure, IngestSuccess, ingest_pdf_path

logger = logging.getLogger("app.api.ingest")
router = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Return system health status and database connectivity."""
    db_status = "connected"
    try:
        with get_db_connection() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1;")
    except Exception as exc:  # noqa: BLE001
        logger.error("Health check database failure", extra={"error": str(exc)})
        db_status = "error"

    registry = get_default_registry()
    return HealthResponse(
        status="ok" if db_status == "connected" else "degraded",
        database=db_status,
        registered_adapters_count=len(registry.list_adapters()),
        version="0.1.0",
    )


@router.post(
    "/ingest/upload",
    response_model=IngestSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": IngestErrorResponse,
            "description": "Invalid payload / bad request",
        },
        422: {
            "model": IngestErrorResponse,
            "description": "Schema, contract, or invariant violation",
        },
    },
)
async def upload_statement(
    file: Annotated[UploadFile, File(...)],
) -> IngestSuccessResponse | JSONResponse:
    """Ingest, extract, reconcile, and persist a financial statement PDF."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported for ingestion.",
        )

    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file payload is empty.",
        )

    if not content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid PDF binary.",
        )

    safe_basename = Path(file.filename).name
    logger.info(
        "Received statement upload",
        extra={"original_basename": safe_basename, "byte_length": len(content)},
    )

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        tmp.write(content)

    try:
        result = ingest_pdf_path(tmp_path, safe_basename)
        if isinstance(result, IngestFailure):
            return JSONResponse(
                status_code=result.http_status,
                content=IngestErrorResponse(
                    status="failed",
                    run_id=result.run_id,
                    raw_payload_id=result.raw_payload_id,
                    adapter_id=result.adapter_id,
                    error_code=result.error_code,
                    detail=result.detail,
                ).model_dump(mode="json"),
            )

        assert isinstance(result, IngestSuccess)
        accounts_summary = [
            AccountSummaryResponse(
                account_id=account_id,
                institution=institution,
                account_mask=mask,
                account_domain=AccountDomain(domain),
                account_type=AccountType(account_type),
                currency=CurrencyCode(currency),
            )
            for (
                account_id,
                institution,
                mask,
                domain,
                account_type,
                currency,
            ) in result.accounts
        ]
        return IngestSuccessResponse(
            status=RunStatus.CANONICAL_PERSISTED,
            run_id=result.run_id,
            raw_payload_id=result.raw_payload_id,
            adapter_id=result.adapter_id,
            adapter_version=result.adapter_version,
            statements_count=result.statements_count,
            transactions_count=result.transactions_count,
            accounts=accounts_summary,
        )
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


@router.get(
    "/ingest/runs/{run_id}",
    response_model=ExtractionRunDetailResponse,
    responses={404: {"description": "Run not found"}},
)
def get_run_status(run_id: UUID) -> ExtractionRunDetailResponse:
    """Retrieve audit details for a specific extraction run without customer PII."""
    with get_db_connection() as conn:
        run = get_extraction_run(conn, run_id)
        if not run:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Extraction run {run_id} not found.",
            )

        bundles = get_run_statements(conn, run_id)
        accounts_summary = [
            AccountSummaryResponse(
                account_id=acc.account_id,
                institution=acc.institution,
                account_mask=acc.account_mask,
                account_domain=acc.account_domain,
                account_type=acc.account_type,
                currency=acc.currency,
            )
            for acc, _, _ in bundles
        ]
        total_txns = sum(txn_count for _, _, txn_count in bundles)

        return ExtractionRunDetailResponse(
            run_id=run.run_id,
            raw_payload_id=run.raw_payload_id,
            adapter_id=run.adapter_id,
            adapter_version=run.adapter_version,
            status=run.status,
            started_at=run.started_at,
            error_code=run.error_code,
            error_message=run.error_message,
            statements_count=len(bundles),
            transactions_count=total_txns,
            accounts=accounts_summary,
        )
