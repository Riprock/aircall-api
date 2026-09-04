"""Resource module for managing messages"""
import warnings
from typing import Optional

from aircall.models import (
    GroupMessage,
    Message,
    SmsTemplate,
    WhatsAppLineStatus,
)
from aircall.pagination import DEFAULT_PER_PAGE, Page
from aircall.resources.base import BaseResource


class MessageResource(BaseResource):
    """
    API Resource for Aircall Messages.

    Handles SMS, MMS, and WhatsApp messaging operations.
    All operations are scoped to a specific number.

    Aircall splits sending into two channels, and the distinction matters:

    - send_in_conversation() stores the message in the agent's Aircall inbox,
      where agents can see and continue the conversation.
    - send_skipping_inbox() bypasses the inbox entirely, for high-volume,
      automated or non-conversational traffic. The number must first be
      registered with create_configuration().
    """

    def create_configuration(self, number_id: int, **kwargs) -> dict:
        """
        Create message configuration for a number.

        Required before the number can use send_skipping_inbox().

        Args:
            number_id: The ID of the number
            **kwargs: Configuration data (callbackUrl, type)

        Returns:
            dict: Configuration response
        """
        return self._post(f"/numbers/{number_id}/messages/configuration", json=kwargs)

    def get_configuration(self, number_id: int) -> dict:
        """
        Fetch message configuration for a number.

        Args:
            number_id: The ID of the number

        Returns:
            dict: Configuration data
        """
        return self._get(f"/numbers/{number_id}/messages/configuration")

    def delete_configuration(self, number_id: int) -> dict:
        """
        Delete message configuration for a number.

        Args:
            number_id: The ID of the number

        Returns:
            dict: Delete configuration response
        """
        return self._delete(f"/numbers/{number_id}/messages/configuration")

    def send_in_conversation(
        self,
        number_id: int,
        to: str,
        body: str,
        media_url: Optional[list[str]] = None,
        **kwargs
    ) -> Message:
        """
        Send a message into the agent conversation.

        The message is stored in the Aircall inbox and is visible to agents
        assigned to the number, who can continue the conversation from there.

        Args:
            number_id: The ID of the number to send from
            to: Recipient phone number, in E.164 format
            body: Message body (max 1600 characters)
            media_url: URLs of media to attach, sent as "mediaUrl"
            **kwargs: Additional body parameters (e.g. agentId)

        Returns:
            Message: The sent message
        """
        return self._send(
            f"/numbers/{number_id}/messages/native/send", to, body, media_url, kwargs
        )

    def send_skipping_inbox(
        self,
        number_id: int,
        to: str,
        body: str,
        media_url: Optional[list[str]] = None,
        **kwargs
    ) -> Message:
        """
        Send a message without storing it in the Aircall inbox.

        For high-volume, automated or non-conversational sending. The message
        does not appear in the agent workspace, and the number must have been
        registered with create_configuration() first.

        Args:
            number_id: The ID of the number to send from
            to: Recipient phone number, in E.164 format
            body: Message body (max 1600 characters)
            media_url: URLs of media to attach, sent as "mediaUrl"
            **kwargs: Additional body parameters

        Returns:
            Message: The sent message
        """
        return self._send(
            f"/numbers/{number_id}/messages/send", to, body, media_url, kwargs
        )

    def _send(
        self,
        endpoint: str,
        to: str,
        body: str,
        media_url: Optional[list[str]],
        extra: dict
    ) -> Message:
        """
        Post a message payload and parse the response.

        Aircall returns the message object at the top level of the response body,
        with no enclosing "message" key.

        Args:
            endpoint: Send endpoint to post to
            to: Recipient phone number
            body: Message body
            media_url: URLs of media to attach, or None
            extra: Additional body parameters

        Returns:
            Message: The sent message
        """
        data = {"to": to, "body": body, **extra}
        if media_url is not None:
            data["mediaUrl"] = media_url
        return Message(**self._post(endpoint, json=data))

    # ------------------------------------------------------------------
    # Group messages
    # ------------------------------------------------------------------

    def send_group_in_conversation(
        self,
        number_id: int,
        participants: list[str],
        body: str,
        **kwargs
    ) -> GroupMessage:
        """
        Send a group message into the agent conversation.

        Stored in the group conversation and visible to agents in their Aircall
        apps.

        Args:
            number_id: The ID of the number to send from
            participants: Recipient phone numbers, in E.164 format
            body: Message body (max 1600 characters)
            **kwargs: Additional body parameters (e.g. agentId)

        Returns:
            GroupMessage: The sent group message
        """
        data = {"participants": participants, "body": body, **kwargs}
        return GroupMessage(
            **self._post(f"/numbers/{number_id}/messages/group/native/send", json=data)
        )

    def send_group_skipping_inbox(
        self,
        number_id: int,
        participants: list[str],
        body: Optional[str] = None,
        media_url: Optional[list[str]] = None,
        **kwargs
    ) -> GroupMessage:
        """
        Send a group message without storing it in the Aircall inbox.

        Aircall accepts text or media per request, not both.

        Args:
            number_id: The ID of the number to send from
            participants: Recipient phone numbers, in E.164 format
            body: Message body (max 1600 characters)
            media_url: URLs of media to attach, sent as "mediaUrl"
            **kwargs: Additional body parameters

        Returns:
            GroupMessage: The sent group message

        Raises:
            ValueError: When neither body nor media_url is supplied
        """
        if body is None and media_url is None:
            raise ValueError("Provide either body or media_url")
        data = {"participants": participants, **kwargs}
        if body is not None:
            data["body"] = body
        if media_url is not None:
            data["mediaUrl"] = media_url
        return GroupMessage(
            **self._post(f"/numbers/{number_id}/messages/group/send", json=data)
        )

    # ------------------------------------------------------------------
    # WhatsApp
    #
    # These two endpoints are NOT scoped under /numbers/:id. They take the
    # number as a lineId body parameter, and they name the recipient field
    # differently from each other.
    # ------------------------------------------------------------------

    def send_whatsapp_in_conversation(
        self,
        number_id: int,
        to: str,
        text: Optional[str] = None,
        template_params: Optional[dict] = None,
        **kwargs
    ) -> Message:
        """
        Send a WhatsApp message into the agent conversation.

        Args:
            number_id: The WhatsApp-capable number to send from, sent as lineId
            to: Recipient phone number, sent as "externalNumber" on this endpoint
            text: Message text (max 4096 characters)
            template_params: Template substitutions, sent as "templateParams".
                Mutually exclusive with text.
            **kwargs: Additional body parameters

        Returns:
            Message: The sent message

        Raises:
            ValueError: When neither or both of text and template_params are given
        """
        data = self._whatsapp_body(number_id, "externalNumber", to, text,
                                   template_params, kwargs)
        return Message(**self._post("/messages/send/whatsapp/native", json=data))

    def send_whatsapp_skipping_inbox(
        self,
        number_id: int,
        to: str,
        text: Optional[str] = None,
        template_params: Optional[dict] = None,
        **kwargs
    ) -> Message:
        """
        Send a WhatsApp message without storing it in the Aircall inbox.

        Args:
            number_id: The WhatsApp-capable number to send from, sent as lineId
            to: Recipient phone number, sent as "to" on this endpoint
            text: Message text (max 4096 characters)
            template_params: Template substitutions, sent as "templateParams".
                Mutually exclusive with text.
            **kwargs: Additional body parameters

        Returns:
            Message: The sent message

        Raises:
            ValueError: When neither or both of text and template_params are given
        """
        data = self._whatsapp_body(number_id, "to", to, text,
                                   template_params, kwargs)
        return Message(**self._post("/messages/whatsapp/send", json=data))

    @staticmethod
    def _whatsapp_body(
        number_id: int,
        recipient_field: str,
        to: str,
        text: Optional[str],
        template_params: Optional[dict],
        extra: dict,
    ) -> dict:
        """
        Build a WhatsApp send body.

        Args:
            number_id: Number to send from, serialised as lineId
            recipient_field: "to" or "externalNumber", depending on the endpoint
            to: Recipient phone number
            text: Message text, or None when sending a template
            template_params: Template substitutions, or None when sending text
            extra: Additional body parameters

        Returns:
            dict: The request body

        Raises:
            ValueError: When neither or both of text and template_params are given
        """
        if (text is None) == (template_params is None):
            raise ValueError(
                "Provide exactly one of text or template_params; Aircall rejects "
                "a request carrying both or neither"
            )
        data = {"lineId": number_id, recipient_field: to, **extra}
        if text is not None:
            data["text"] = text
        else:
            data["templateParams"] = template_params
        return data

    # ------------------------------------------------------------------
    # Templates and channel status
    # ------------------------------------------------------------------

    def list_sms_templates(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PER_PAGE,
        search: Optional[str] = None,
    ) -> Page:
        """
        List the company's SMS templates, aggregated across all agents.

        Args:
            page: Page number (default 1)
            per_page: Templates per page. This endpoint allows up to 100,
                unlike the 50 most Aircall list endpoints cap at.
            search: Free-text search across template name and body

        Returns:
            Page: SmsTemplate objects
        """
        params = {"search": search} if search is not None else None
        return self._list(
            "/sms/templates", "templates", SmsTemplate,
            page=page, per_page=per_page, params=params, max_per_page=100,
        )

    def list_whatsapp_templates(self, number_id: int, **params) -> dict:
        """
        List WhatsApp templates for a WhatsApp-capable number.

        Returned raw: this endpoint uses cursor pagination and returns a
        "pageInfo" object with a nextToken, rather than the "meta" envelope the
        rest of the API uses, so it does not map onto Page.

        Args:
            number_id: The ID of the number
            **params: Query filters -- status, category, token (cursor),
                limit, sort

        Returns:
            dict: {"templates": [...], "pageInfo": {...}}
        """
        return self._get(f"/numbers/{number_id}/templates", params=params or None)

    def get_whatsapp_status(self, number_id: int) -> WhatsAppLineStatus:
        """
        Get the WhatsApp registration and health status of a number.

        Args:
            number_id: The ID of the number

        Returns:
            WhatsAppLineStatus: Registration status, quality rating and limits
        """
        return WhatsAppLineStatus(
            **self._get(f"/numbers/{number_id}/whatsapp_status")
        )

    def send(self, number_id: int, to: str, body: str, **kwargs) -> Message:
        """
        Deprecated alias for send_skipping_inbox().

        .. deprecated:: 2.0.0
            The name did not say which channel it used. This method skips the
            Aircall inbox; use send_skipping_inbox(), or send_in_conversation()
            if you meant the agent-visible one.

        Args:
            number_id: The ID of the number to send from
            to: Recipient phone number
            body: Message body
            **kwargs: Additional body parameters

        Returns:
            Message: The sent message
        """
        warnings.warn(
            "MessageResource.send() is deprecated; it skips the Aircall inbox. "
            "Use send_skipping_inbox(), or send_in_conversation() for the "
            "agent-visible channel.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.send_skipping_inbox(number_id, to, body, **kwargs)

    def send_native(self, number_id: int, **kwargs) -> Message:
        """
        Deprecated alias for send_in_conversation().

        .. deprecated:: 2.0.0
            "native" did not describe the behaviour, and the old docstring
            wrongly described this as a WhatsApp template endpoint. It sends a
            message into the agent conversation.

        Args:
            number_id: The ID of the number to send from
            **kwargs: Body parameters, including to and body

        Returns:
            Message: The sent message
        """
        warnings.warn(
            "MessageResource.send_native() is deprecated; it sends into the "
            "agent conversation. Use send_in_conversation().",
            DeprecationWarning,
            stacklevel=2,
        )
        to = kwargs.pop("to", None)
        body = kwargs.pop("body", None)
        return self.send_in_conversation(number_id, to, body, **kwargs)
