"""Aircall API resource classes."""

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

__all__ = [
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
]
