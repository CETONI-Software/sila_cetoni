from typing import TYPE_CHECKING

from .digitalinchannelprovider_base import DigitalInChannelProviderBase
from .digitalinchannelprovider_errors import InvalidChannelIndex
from .digitalinchannelprovider_feature import DigitalInChannelProviderFeature
from .digitalinchannelprovider_types import State

__all__ = [
    "DigitalInChannelProviderBase",
    "DigitalInChannelProviderFeature",
    "InvalidChannelIndex",
    "State",
]

if TYPE_CHECKING:
    from .digitalinchannelprovider_client import DigitalInChannelProviderClient  # noqa: F401

    __all__.append("DigitalInChannelProviderClient")
