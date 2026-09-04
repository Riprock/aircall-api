"""Resource module for Analytics report exports"""

from aircall.models import AnalyticsExport
from aircall.models.analytics import RELATIVE_DATE_RANGES, REPORT_NAMES
from aircall.resources.base import BaseResource


class AnalyticsResource(BaseResource):
    """
    API Resource for Aircall Analytics report exports.

    Reports are generated asynchronously: create an export job, poll it until it
    leaves PENDING, then download the file from the presigned URL.

    Requires the Analytics+ entitlement; without it Aircall returns 403.
    """

    def create_export(
        self,
        report_name: str,
        timezone: str,
        relative_range: str | None = None,
        absolute_range: dict | None = None,
        filters: dict | None = None,
        options: dict | None = None,
        export_options: dict | None = None,
    ) -> AnalyticsExport:
        """
        Submit an asynchronous report export job.

        Exactly one of relative_range or absolute_range must be given; Aircall
        rejects a request carrying both or neither.

        Args:
            report_name: One of REPORT_NAMES, e.g. "CALLS_HISTORY"
            timezone: IANA timezone resolving the date window and bucketing
                date-breakdown rows, e.g. "Europe/Paris". Mandatory.
            relative_range: A pre-defined window from RELATIVE_DATE_RANGES,
                e.g. "LAST_WEEK"
            absolute_range: {"fromDate": "YYYY-MM-DD", "toDate": "YYYY-MM-DD"}
            filters: Further filters merged into the filter object -- userIDs,
                teamIDs, teamFilterOption, hours, callIDs, lineIDs,
                customerNumbers, tagIDs, callTypes, duration,
                minConnectedDuration, ivrBranches, virtualVoiceAgentIDs,
                withAiIntervention, withVoicemail, ringAttemptOrigin,
                userStatuses, nextUserStatuses. Array filters always take a
                list, even for a single value.
            options: Report options -- dateBreakdown, slaTimeToAnswerInSeconds,
                slaIncludedCallUnansweredReasons
            export_options: File options -- format (CSV), exportName

        Returns:
            AnalyticsExport: The created job, initially status PENDING

        Raises:
            ValueError: When report_name is unknown, when the date range is not
                exactly one of relative or absolute, or when relative_range is
                not a value Aircall accepts
        """
        if report_name not in REPORT_NAMES:
            raise ValueError(
                f"report_name must be one of {list(REPORT_NAMES)}, got {report_name!r}"
            )
        if (relative_range is None) == (absolute_range is None):
            raise ValueError(
                "Provide exactly one of relative_range or absolute_range"
            )
        if relative_range is not None and relative_range not in RELATIVE_DATE_RANGES:
            raise ValueError(
                f"relative_range must be one of {list(RELATIVE_DATE_RANGES)}, "
                f"got {relative_range!r}"
            )

        date_filter = (
            {"relative": relative_range} if relative_range is not None
            else {"absoluteRange": absolute_range}
        )
        payload = {
            "reportName": report_name,
            "filter": {
                "dateFilter": date_filter,
                "timezone": timezone,
                **(filters or {}),
            },
        }
        if options is not None:
            payload["options"] = options
        if export_options is not None:
            payload["exportOptions"] = export_options

        response = self._post("/analytics/report/export", json={"input": payload})
        return AnalyticsExport(**response)

    def get_export(self, export_id: str) -> AnalyticsExport:
        """
        Fetch the current state of an export job.

        Poll roughly once a minute while the status is PENDING. The downloadUrl
        is presigned and expires about an hour after completion -- call this
        again to mint a fresh one while the export still exists.

        A FAILED status is usually deterministic (invalid filters, unsupported
        combinations); read errorMessage before retrying the same payload.

        Args:
            export_id: The export job's ID, from create_export()

        Returns:
            AnalyticsExport: The job, with downloadUrl once COMPLETED
        """
        response = self._get(f"/analytics/report/export/{export_id}")
        return AnalyticsExport(**response)
