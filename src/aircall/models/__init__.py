"""Aircall API models."""

# Core resources
from aircall.models.call import Call, CallComment
from aircall.models.company import Company
from aircall.models.contact import Contact, Email, PhoneNumber
from aircall.models.number import Number, NumberMessages
from aircall.models.tag import Tag
from aircall.models.team import Team
from aircall.models.user import User, UserAvailability

# AI and Intelligence
from aircall.models.ai_voice_agent import AIVoiceAgent
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
from aircall.models.message import MediaDetail, Message
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
