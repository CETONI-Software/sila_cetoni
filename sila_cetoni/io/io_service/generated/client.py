from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .analoginchannelprovider import AnalogInChannelProviderFeature, InvalidChannelIndex
from .analogoutchannelcontroller import AnalogOutChannelControllerFeature, InvalidChannelIndex
from .digitalinchannelprovider import DigitalInChannelProviderFeature, InvalidChannelIndex
from .digitaloutchannelcontroller import DigitalOutChannelControllerFeature, InvalidChannelIndex

if TYPE_CHECKING:

    from .analoginchannelprovider import AnalogInChannelProviderClient
    from .analogoutchannelcontroller import AnalogOutChannelControllerClient
    from .digitalinchannelprovider import DigitalInChannelProviderClient
    from .digitaloutchannelcontroller import DigitalOutChannelControllerClient


class Client(SilaClient):

    AnalogInChannelProvider: AnalogInChannelProviderClient

    AnalogOutChannelController: AnalogOutChannelControllerClient

    DigitalInChannelProvider: DigitalInChannelProviderClient

    DigitalOutChannelController: DigitalOutChannelControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            AnalogInChannelProviderFeature.defined_execution_errors["InvalidChannelIndex"], InvalidChannelIndex
        )

        self._register_defined_execution_error_class(
            AnalogOutChannelControllerFeature.defined_execution_errors["InvalidChannelIndex"], InvalidChannelIndex
        )

        self._register_defined_execution_error_class(
            DigitalInChannelProviderFeature.defined_execution_errors["InvalidChannelIndex"], InvalidChannelIndex
        )

        self._register_defined_execution_error_class(
            DigitalOutChannelControllerFeature.defined_execution_errors["InvalidChannelIndex"], InvalidChannelIndex
        )
