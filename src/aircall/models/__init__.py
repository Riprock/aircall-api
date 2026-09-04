"""Aircall API models."""

# Core resources
from aircall.models.call import Call, CallComment
from aircall.models.company import Company
from aircall.models.contact import Contact, Email, PhoneNumber
from aircall.models.number import Number, NumberMessages
from aircall.models.tag import Tag
from aircall.models.team import Team
from aircall.models.user import User, UserAvailability
from aircall.models.userv2 import UserV2, UserV2Availability

# AI and Intelligence
from aircall.models.ai_voice_agent import (
    AIVoiceAgent,
    CallAIVoiceAgent,
    OutboundCallRequest,
)
from aircall.models.analytics import AnalyticsExport
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

# Communication
from aircall.models.message import (
    GroupMessage,
    MediaDetail,
    Message,
    SmsTemplate,
    WhatsAppLineStatus,
)
from aircall.models.webhook import Webhook

# Campaign and Compliance
from aircall.models.dialer_campaign import DialerCampaign, DialerCampaignPhoneNumber

# Call-related
from aircall.models.ivr_option import IVROption
from aircall.models.participant import (
    ConversationIntelligenceParticipant,
    Participant,
)

# Integration
from aircall.models.integration import Integration

__all__ = [
    # Core resources
    "User",
    "UserAvailability",
    "UserV2",
    "UserV2Availability",
    "Call",
    "CallComment",
    "Contact",
    "PhoneNumber",
    "Email",
    "Number",
    "NumberMessages",
    "Team",
    "Tag",
    "Company",
    # AI and Intelligence
    "AIVoiceAgent",
    "CallAIVoiceAgent",
    "OutboundCallRequest",
    "AnalyticsExport",
    "ConversationIntelligence",
    "RealtimeTranscription",
    "RealtimeTranscriptionCall",
    "RealtimeTranscriptionUtterance",
    "Content",
    "Utterance",
    "SummaryContent",
    "TopicsContent",
    "ActionItemsContent",
    # Communication
    "Message",
    "MediaDetail",
    "GroupMessage",
    "SmsTemplate",
    "WhatsAppLineStatus",
    "Webhook",
    # Campaign and Compliance
    "DialerCampaign",
    "DialerCampaignPhoneNumber",
    # Call-related
    "Participant",
    "ConversationIntelligenceParticipant",
    "IVROption",
    # Integration
    "Integration",
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
