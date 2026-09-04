"""Resource module for triggering AI Voice Agent outbound calls"""

from aircall.models import OutboundCallRequest
from aircall.resources.base import BaseResource


class AIVoiceAgentResource(BaseResource):
    """
    API Resource for Call AI Voice Agents.

    An Outbound Voice Agent places calls to contacts on behalf of the company,
    triggered by an external system such as a CRM or scheduling tool. Typical
    uses are appointment reminders, billing follow-ups and lead qualification.

    The agent must already be configured in the Aircall Dashboard with a
    connected phone number and a first message.

    Calls are queued rather than placed immediately: a company may have 5
    concurrent agent calls, and each agent's number may host only 1.
    """

    def trigger_outbound_call(
        self,
        agent_id: str,
        contact_phone: str,
        idempotency_key: str,
        context: dict | None = None,
        expiration_seconds: int | None = None,
    ) -> OutboundCallRequest:
        """
        Queue an outbound call from an AI Voice Agent.

        Every ``{{variable}}`` in the agent's first message and voicemail message
        must have a matching key in ``context``, or Aircall rejects the call. A
        context value that is a UTC datetime in ISO 8601 form is converted to
        natural language, and then a ``timezone`` key is required alongside it.

        Args:
            agent_id: The Outbound Voice Agent's identifier
            contact_phone: Number to call, in E.164 format
            idempotency_key: Caller-supplied key that makes retries safe.
                Reusing one returns 409.
            context: Values filling the agent's {{variable}} placeholders
            expiration_seconds: How long to keep trying if the concurrency limit
                is reached. 60 to 86400, Aircall defaults to 3600.

        Returns:
            OutboundCallRequest: The queued request, initially status PENDING

        Raises:
            ValueError: When expiration_seconds is outside 60-86400
        """
        if expiration_seconds is not None and not 60 <= expiration_seconds <= 86400:
            raise ValueError(
                "expiration_seconds must be between 60 and 86400, "
                f"got {expiration_seconds}"
            )
        data = {
            "contact_phone": contact_phone,
            "idempotency_key": idempotency_key,
        }
        if context is not None:
            data["context"] = context
        if expiration_seconds is not None:
            data["expiration_seconds"] = expiration_seconds
        response = self._post(f"/outbound-calls/agents/{agent_id}", json=data)
        return OutboundCallRequest(**response)
