"""Resource module for managing calls"""
from typing import Optional

from aircall.deprecation import (
    REALTIME_TRANSCRIPTION_SUNSET,
    warn_deprecated,
)
from aircall.pagination import DEFAULT_PER_PAGE, Page
from aircall.resources.base import BaseResource
from aircall.models import Call

#: Values Aircall accepts for the transcription "mode" query param.
TRANSCRIPTION_MODES = frozenset({"async", "realtime"})


class CallResource(BaseResource):
    """
    API Resource for Aircall Calls

    Handles operations relating to calls including status, voicemails, insights and summaries
    """
    def list_calls(
        self, page: int = 1, per_page: int = DEFAULT_PER_PAGE, **params
    ) -> Page:
        """
        List all calls with pagination.

        Only six months of history is available, and pagination caps out at
        10,000 calls -- use the ``from`` filter to reach older calls.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)
            **params: Query filters. Aircall accepts:
                from (int): minimum creation date, UNIX timestamp
                to (int): maximum creation date, UNIX timestamp
                order (str): "asc" or "desc" by created_at (default "asc")
                fetch_contact (bool): include contact details
                fetch_short_urls (bool): include recording/voicemail short URLs
                fetch_call_timeline (bool): include ivr_options_selected
                fetch_aiva_conv (bool): include ai_voice_agents

        Returns:
            Page: Call objects, carrying .meta pagination details
        """
        return self._list(
            "/calls", "calls", Call, page=page, per_page=per_page, params=params
        )

    def get(self, call_id: int, **params) -> Call:
        """
        Get a specific call by ID.

        Args:
            call_id: The ID of the call to retrieve
            **params: Query toggles -- fetch_contact, fetch_short_urls,
                fetch_call_timeline, fetch_aiva_conv

        Returns:
            Call: The call object
        """
        response = self._get(f"/calls/{call_id}", params=params or None)
        return Call(**response["call"])

    def search(self, page: int = 1, per_page: int = DEFAULT_PER_PAGE, **params) -> Page:
        """
        Search for calls with various filters.

        Args:
            page: Page number (default 1)
            per_page: Results per page (1-50, default 20)
            **params: Search filters. Accepts the same options as list_calls()
                (from, to, order, fetch_contact, fetch_short_urls,
                fetch_call_timeline, fetch_aiva_conv) plus search terms.

        Returns:
            Page: matching Call objects, carrying .meta pagination details
        """
        return self._list(
            "/calls/search", "calls", Call, page=page, per_page=per_page, params=params
        )

    def transfer(self, call_id: int, number_id: int, comment: str = None) -> dict:
        """
        Transfer a call to another number.

        Args:
            call_id: The ID of the call to transfer
            number_id: The ID of the number to transfer to
            comment: Optional comment for the transfer

        Returns:
            dict: Transfer response
        """
        self._logger.info("Transferring call %s to number %s", call_id, number_id)
        data = {"number_id": number_id}
        if comment:
            data["comment"] = comment
        result = self._post(f"/calls/{call_id}/transfers", json=data)
        self._logger.info("Successfully transferred call %s", call_id)
        return result

    def add_comment(self, call_id: int, content: str) -> dict:
        """
        Add a comment to a call.

        Args:
            call_id: The ID of the call
            content: The comment content

        Returns:
            dict: Comment response
        """
        return self._post(f"/calls/{call_id}/comments", json={"content": content})

    def add_tags(self, call_id: int, tags: list[str]) -> dict:
        """
        Add tags to a call.

        Args:
            call_id: The ID of the call
            tags: List of tag names to add

        Returns:
            dict: Tags response
        """
        return self._post(f"/calls/{call_id}/tags", json={"tags": tags})

    def archive(self, call_id: int) -> dict:
        """
        Archive a call.

        Args:
            call_id: The ID of the call to archive

        Returns:
            dict: Archive response
        """
        return self._put(f"/calls/{call_id}/archive")

    def unarchive(self, call_id: int) -> dict:
        """
        Unarchive a call.

        Args:
            call_id: The ID of the call to unarchive

        Returns:
            dict: Unarchive response
        """
        return self._put(f"/calls/{call_id}/unarchive")

    def pause_recording(self, call_id: int) -> dict:
        """
        Pause recording for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Pause recording response
        """
        return self._post(f"/calls/{call_id}/pause_recording")

    def resume_recording(self, call_id: int) -> dict:
        """
        Resume recording for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Resume recording response
        """
        return self._post(f"/calls/{call_id}/resume_recording")

    def delete_recording(self, call_id: int) -> dict:
        """
        Delete the recording of a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Delete recording response
        """
        self._logger.warning("Deleting recording for call %s", call_id)
        result = self._delete(f"/calls/{call_id}/recording")
        self._logger.info("Successfully deleted recording for call %s", call_id)
        return result

    def delete_voicemail(self, call_id: int) -> dict:
        """
        Delete the voicemail of a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Delete voicemail response
        """
        self._logger.warning("Deleting voicemail for call %s", call_id)
        result = self._delete(f"/calls/{call_id}/voicemail")
        self._logger.info("Successfully deleted voicemail for call %s", call_id)
        return result

    def add_insight_cards(self, call_id: int, cards: list[dict]) -> dict:
        """
        Add insight cards to a call.

        Args:
            call_id: The ID of the call
            cards: List of insight card objects

        Returns:
            dict: Insight cards response
        """
        return self._post(f"/calls/{call_id}/insight_cards", json={"cards": cards})

    def get_transcription(self, call_id: int, mode: Optional[str] = None) -> dict:
        """
        Get the transcription of a call.

        This is the migration target for get_realtime_transcription(): pass
        mode="realtime" to fetch the transcription generated for the agent
        during the call.

        Args:
            call_id: The ID of the call
            mode: Transcription mode, "async" or "realtime". Omit for Aircall's
                default.

        Returns:
            dict: Transcription data

        Raises:
            ValueError: When mode is not one Aircall accepts
        """
        if mode is not None and mode not in TRANSCRIPTION_MODES:
            raise ValueError(
                f"mode must be one of {sorted(TRANSCRIPTION_MODES)}, got {mode!r}"
            )
        params = {"mode": mode} if mode is not None else None
        return self._get(f"/calls/{call_id}/transcription", params=params)

    def get_realtime_transcription(self, call_id: int) -> dict:
        """
        Get the real-time transcription of a call.

        .. deprecated:: 2.0.0
            Aircall's removal date for this endpoint was 2026-03-31 and has
            passed. Use ``get_transcription(call_id, mode="realtime")``.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Real-time transcription data
        """
        warn_deprecated(
            "CallResource.get_realtime_transcription()",
            'get_transcription(call_id, mode="realtime")',
            REALTIME_TRANSCRIPTION_SUNSET,
        )
        return self._get(f"/calls/{call_id}/realtime_transcription")

    def get_predicted_csat(self, call_id: int) -> dict:
        """
        Retrieve the Predicted CSAT score and its drivers for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: {"csat": {"score": int, "drivers": [...], ...}}
        """
        return self._get(f"/calls/{call_id}/predicted_csat")

    def get_custom_summary_result(self, call_id: int) -> dict:
        """
        Retrieve the custom summary result for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: The custom summary, including summary_template_results
        """
        return self._get(f"/calls/{call_id}/custom_summary_result")

    def get_sentiments(self, call_id: int) -> dict:
        """
        Get sentiment analysis for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Sentiment analysis data
        """
        return self._get(f"/calls/{call_id}/sentiments")

    def get_topics(self, call_id: int) -> dict:
        """
        Get topics discussed in a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Topics data
        """
        return self._get(f"/calls/{call_id}/topics")

    def get_summary(self, call_id: int) -> dict:
        """
        Get the summary of a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Call summary data
        """
        return self._get(f"/calls/{call_id}/summary")

    def get_action_items(self, call_id: int) -> dict:
        """
        Get action items from a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Action items data
        """
        return self._get(f"/calls/{call_id}/action_items")

    def get_playbook_result(
        self, call_id: int, fetch_playbook: Optional[bool] = None
    ) -> dict:
        """
        Get playbook results for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Playbook result data
        """
        params = {"fetch_playbook": fetch_playbook} if fetch_playbook is not None else None
        return self._get(f"/calls/{call_id}/playbook_result", params=params)

    def get_evaluation(self, call_id: int) -> dict:
        """
        Use this endpoint to retrieve the evaluations for a specific call.

        Args:
            call_id: The ID of the call
        """
        return self._get(f"/calls/{call_id}/evaluations")