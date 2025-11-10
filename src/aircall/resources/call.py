"""Resource module for managing calls"""
from aircall.resources.base import BaseResource
from aircall.models import Call

class CallResource(BaseResource):
    """
    API Resource for Aircall Calls

    Handles operations relating to calls including status, voicemails, insights and summaries
    """
    def list_calls(self, page: int = 1, per_page: int = 20) -> list[Call]:
        """
        List all calls with pagination.

        Args:
            page: Page number (default 1)
            per_page: Results per page (default 20, max 50)

        Returns:
            list[Call]: List of Call objects
        """
        response = self._get("/calls", params={"page": page, "per_page": per_page})
        return [Call(**c) for c in response["calls"]]

    def get(self, call_id: int) -> Call:
        """
        Get a specific call by ID.

        Args:
            call_id: The ID of the call to retrieve

        Returns:
            Call: The call object
        """
        response = self._get(f"/calls/{call_id}")
        return Call(**response["call"])

    def search(self, **params) -> list[Call]:
        """
        Search for calls with various filters.

        Args:
            **params: Search parameters (from, to, tags, etc.)

        Returns:
            list[Call]: List of Call objects matching the search criteria
        """
        response = self._get("/calls/search", params=params)
        return [Call(**c) for c in response["calls"]]

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

    def get_transcription(self, call_id: int) -> dict:
        """
        Get the transcription of a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Transcription data
        """
        return self._get(f"/calls/{call_id}/transcription")

    def get_realtime_transcription(self, call_id: int) -> dict:
        """
        Get the real-time transcription of a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Real-time transcription data
        """
        return self._get(f"/calls/{call_id}/realtime_transcription")

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

    def get_playbook_result(self, call_id: int) -> dict:
        """
        Get playbook results for a call.

        Args:
            call_id: The ID of the call

        Returns:
            dict: Playbook result data
        """
        return self._get(f"/calls/{call_id}/playbook_result")
