"""Aircall API resource classes."""

from aircall.resources.ai_voice_agent import AIVoiceAgentResource
from aircall.resources.analytics import AnalyticsResource
from aircall.resources.base import BaseResource
from aircall.resources.call import CallResource
from aircall.resources.company import CompanyResource
from aircall.resources.contact import ContactResource
from aircall.resources.dialer_campaign import DialerCampaignResource
from aircall.resources.integration import IntegrationResource
from aircall.resources.message import MessageResource
from aircall.resources.number import NumberResource
from aircall.resources.tag import TagResource
from aircall.resources.team import TeamResource
from aircall.resources.user import UserResource
from aircall.resources.webhook import WebhookResource
from aircall.resources.userv2 import UserV2Resource

__all__ = [
    "AIVoiceAgentResource",
    "AnalyticsResource",
    "BaseResource",
    "CallResource",
    "CompanyResource",
    "ContactResource",
    "DialerCampaignResource",
    "IntegrationResource",
    "MessageResource",
    "NumberResource",
    "TagResource",
    "TeamResource",
    "UserResource",
    "WebhookResource",
    "UserV2Resource"
]
