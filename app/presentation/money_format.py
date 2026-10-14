"""Format integer cents as USD for UI display.

Storage and arithmetic remain integer cents. This module performs only
integer division for presentation — never ``float`` monetary math.
"""

from __future__ import annotations


def format_usd_cents(amount_cents: int) -> str:
    """Return a USD string like ``$1,295.00`` or ``-$10.50`` from integer cents.

    Raises:
        TypeError: If ``amount_cents`` is not a true ``int`` (rejects ``bool``,
            ``float``, and numeric strings).
    """
    if type(amount_cents) is not int:
        raise TypeError(
            f"amount_cents must be int cents, got {type(amount_cents).__name__}"
        )

    sign = "-" if amount_cents < 0 else ""
    absolute = abs(amount_cents)
    dollars, cents = divmod(absolute, 100)
    return f"{sign}${dollars:,}.{cents:02d}"
