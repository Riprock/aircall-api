"""Analytics models for Aircall API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

#: Report types accepted by Create an Analytics Report Export.
REPORT_NAMES = (
    "CALLS_HISTORY",
    "USER_STATUS_HISTORY",
    "USER_ACTIVITY_AVAILABILITY_BREAKDOWN",
    "USER_ACTIVITY_AVERAGE_AFTER_CALL_WORK_TIME_PER_USER",
    "USER_ACTIVITY_AVERAGE_INBOUND_IN_CALL_TIME_PER_USER",
    "USER_ACTIVITY_AVERAGE_OUTBOUND_IN_CALL_TIME_PER_USER",
    "USER_ACTIVITY_CALL_VOLUME_AND_TIME",
    "USER_ACTIVITY_CALLS_HANDLED",
    "USER_ACTIVITY_PERCENTAGE_OF_TIME_IN_EACH_STATUS",
    "USER_ACTIVITY_RINGING_ATTEMPTS_PER_USER",
    "USER_ACTIVITY_WORK_TIME_AND_AVAILABILITY",
    "USER_ACTIVITY_RINGING_ATTEMPTS",
)

#: Pre-defined date windows for dateFilter.relative.
RELATIVE_DATE_RANGES = (
    "LAST_MONTH", "LAST_WEEK", "THIS_MONTH", "THIS_WEEK", "TODAY", "YESTERDAY",
)


class AnalyticsExport(BaseModel):
    """
    An asynchronous Analytics report export job.

    Reports are generated asynchronously: create the job, poll until it leaves
    PENDING, then download from the presigned URL. Requires the Analytics+
    entitlement.

    Aircall returns camelCase field names on these endpoints, unlike the
    snake_case used across the rest of the API.
    """

    exportID: str
    createdAt: Optional[datetime] = None
    status: Optional[Literal["PENDING", "COMPLETED", "FAILED"]] = None
    format: Optional[str] = None
    exportName: Optional[str] = None
    isZipCompressed: Optional[bool] = None
    # Present only once status is COMPLETED; presigned and time-limited.
    downloadUrl: Optional[str] = None
    downloadUrlExpiresAt: Optional[datetime] = None
    # Present only when status is FAILED.
    errorMessage: Optional[str] = None

    @property
    def is_complete(self) -> bool:
        """Whether the export finished successfully and can be downloaded."""
        return self.status == "COMPLETED"

    @property
    def is_pending(self) -> bool:
        """Whether the export is still being generated and should be polled."""
        return self.status == "PENDING"

    @property
    def is_failed(self) -> bool:
        """Whether the export failed. Read errorMessage before retrying."""
        return self.status == "FAILED"
