from typing import TYPE_CHECKING

from .analoginchannelprovider_base import AnalogInChannelProviderBase
from .analoginchannelprovider_errors import InvalidChannelIndex
from .analoginchannelprovider_feature import AnalogInChannelProviderFeature

__all__ = [
    "AnalogInChannelProviderBase",
    "AnalogInChannelProviderFeature",
    "InvalidChannelIndex",
]

if TYPE_CHECKING:
    from .analoginchannelprovider_client import AnalogInChannelProviderClient  # noqa: F401

    __all__.append("AnalogInChannelProviderClient")
