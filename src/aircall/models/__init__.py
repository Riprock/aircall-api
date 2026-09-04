"""Aircall API models."""

# Core resources
# AI and Intelligence
from aircall.models.ai_voice_agent import (
    AIVoiceAgent,
    CallAIVoiceAgent,
    OutboundCallRequest,
)
from aircall.models.analytics import AnalyticsExport
from aircall.models.call import Call, CallComment
from aircall.models.company import Company
from aircall.models.contact import Contact, Email, PhoneNumber
from aircall.models.content import (
    ActionItemsContent,
    Content,
    SummaryContent,
    TopicsContent,
    Utterance,
)
from aircall.models.conversation_intelligence import (
    ConversationIntelligence,
    RealtimeTranscription,
    RealtimeTranscriptionCall,
    RealtimeTranscriptionUtterance,
)

# Campaign and Compliance
from aircall.models.dialer_campaign import DialerCampaign, DialerCampaignPhoneNumber

# Integration
from aircall.models.integration import Integration

# Call-related
from aircall.models.ivr_option import IVROption

# Communication
from aircall.models.message import (
    GroupMessage,
    MediaDetail,
    Message,
    SmsTemplate,
    WhatsAppLineStatus,
)
from aircall.models.number import Number, NumberMessages
from aircall.models.participant import (
    ConversationIntelligenceParticipant,
    Participant,
)
from aircall.models.tag import Tag
from aircall.models.team import Team
from aircall.models.user import User, UserAvailability
from aircall.models.userv2 import UserV2, UserV2Availability
from aircall.models.webhook import Webhook

__all__ = [
    "AIVoiceAgent",
    "ActionItemsContent",
    "AnalyticsExport",
    "Call",
    "CallAIVoiceAgent",
    "CallComment",
    "Company",
    "Contact",
    "Content",
    "ConversationIntelligence",
    "ConversationIntelligenceParticipant",
    "DialerCampaign",
    "DialerCampaignPhoneNumber",
    "Email",
    "GroupMessage",
    "IVROption",
    "Integration",
    "MediaDetail",
    "Message",
    "Number",
    "NumberMessages",
    "OutboundCallRequest",
    "Participant",
    "PhoneNumber",
    "RealtimeTranscription",
    "RealtimeTranscriptionCall",
    "RealtimeTranscriptionUtterance",
    "SmsTemplate",
    "SummaryContent",
    "Tag",
    "Team",
    "TopicsContent",
    "User",
    "UserAvailability",
    "UserV2",
    "UserV2Availability",
    "Utterance",
    "Webhook",
    "WhatsAppLineStatus",
]


# ---------------------------------------------------------------------------
# Forward reference resolution
#
# User and Number reference each other, so one of the two must annotate the
# relationship as a string forward ref (User.numbers -> list["Number"]) and
# import the other only under TYPE_CHECKING. Pydantic cannot resolve that ref
# from user.py's module globals, which leaves User -- and every model built on
# it (Call, CallComment, Team, Message, Integration) -- incomplete, raising
# "`User` is not fully defined" on the first validation instead of at import.
#
# This module is the one place where every model is in scope, and it always
# runs before any submodule is importable, so resolve the refs here. Order
# matters: User must be rebuilt before the models that embed it.
# Covered by tests/test_models_resolve.py.
# ---------------------------------------------------------------------------
for _model in (
    User,
    Number,
    Call,
    CallComment,
    Team,
    Message,
    GroupMessage,
    Integration,
    Contact,
):
    _model.model_rebuild()

del _model
