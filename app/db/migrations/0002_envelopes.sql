-- YNAB budgets / envelopes: named envelopes with integer-cent balances.
-- Ready to Assign is derived (Vault closings − SUM(balance_cents)), not stored.

CREATE TABLE IF NOT EXISTS envelopes (
  envelope_id    UUID PRIMARY KEY,
  name           TEXT NOT NULL,
  balance_cents  BIGINT NOT NULL DEFAULT 0 CHECK (balance_cents >= 0),
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (char_length(btrim(name)) > 0)
);

CREATE UNIQUE INDEX IF NOT EXISTS envelopes_name_uidx
  ON envelopes (lower(btrim(name)));
