"""Deprecation warnings for Aircall API surfaces being retired.

Aircall publishes a removal date for each deprecated endpoint. Emitting a
warning that names both the replacement and that date lets callers see what is
going away, and whether they are already past the deadline, without reading the
changelog.
"""

import warnings
from datetime import UTC, date, datetime

#: Aircall retires the User V1 list/retrieve/create/update endpoints on this date.
USER_V1_SUNSET = "2026-09-30"

#: Aircall's removal date for the realtime_transcription endpoint.
REALTIME_TRANSCRIPTION_SUNSET = "2026-03-31"


def warn_deprecated(
    what: str, replacement: str, sunset: str, stacklevel: int = 3
) -> None:
    """
    Emit a DeprecationWarning naming the replacement and Aircall's removal date.

    Args:
        what: The deprecated method, e.g. "UserResource.get()"
        replacement: What to use instead
        sunset: Aircall's removal date, ISO 8601 (YYYY-MM-DD)
        stacklevel: Frames to skip so the warning points at the caller's code.
            The default of 3 is correct for a resource method calling this
            directly.
    """
    today = datetime.now(UTC).date()
    if date.fromisoformat(sunset) < today:
        timing = f"Aircall's removal date of {sunset} has passed"
    else:
        timing = f"Aircall removes it on {sunset}"
    warnings.warn(
        f"{what} is deprecated; {timing}. Use {replacement} instead.",
        DeprecationWarning,
        stacklevel=stacklevel,
    )
