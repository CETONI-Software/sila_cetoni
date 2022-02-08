from typing import List, Optional, Union
from uuid import UUID

from qmixsdk.qmixanalogio import AnalogInChannel, AnalogOutChannel
from qmixsdk.qmixdigio import DigitalInChannel, DigitalOutChannel

from ...core.core_service.server import Server as CoreServer
from .feature_implementations.analoginchannelprovider_impl import AnalogInChannelProviderImpl
from .feature_implementations.analogoutchannelcontroller_impl import AnalogOutChannelControllerImpl
from .feature_implementations.digitalinchannelprovider_impl import DigitalInChannelProviderImpl
from .feature_implementations.digitaloutchannelcontroller_impl import DigitalOutChannelControllerImpl
from .generated.analoginchannelprovider import AnalogInChannelProviderFeature
from .generated.analogoutchannelcontroller import AnalogOutChannelControllerFeature
from .generated.digitalinchannelprovider import DigitalInChannelProviderFeature
from .generated.digitaloutchannelcontroller import DigitalOutChannelControllerFeature


class Server(CoreServer):
    def __init__(
        self,
        io_channels: List[Union[AnalogInChannel, AnalogOutChannel, DigitalInChannel, DigitalOutChannel]],
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        super().__init__(
            server_name=server_name or "I/O Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI I/O modules",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        analog_in_channels = list(filter(lambda c: isinstance(c, AnalogInChannel), io_channels))
        analog_out_channels = list(filter(lambda c: isinstance(c, AnalogOutChannel), io_channels))
        digital_in_channels = list(filter(lambda c: isinstance(c, DigitalInChannel), io_channels))
        digital_out_channels = list(filter(lambda c: isinstance(c, DigitalOutChannel), io_channels))

        if analog_in_channels:
            self.analoginchannelprovider = AnalogInChannelProviderImpl(analog_in_channels, self.child_task_executor)
            self.set_feature_implementation(AnalogInChannelProviderFeature, self.analoginchannelprovider)
        if analog_out_channels:
            self.analogoutchannelcontroller = AnalogOutChannelControllerImpl(
                analog_out_channels, self.child_task_executor
            )
            self.set_feature_implementation(AnalogOutChannelControllerFeature, self.analogoutchannelcontroller)
        if digital_in_channels:
            self.digitalinchannelprovider = DigitalInChannelProviderImpl(digital_in_channels, self.child_task_executor)
            self.set_feature_implementation(DigitalInChannelProviderFeature, self.digitalinchannelprovider)
        if digital_out_channels:
            self.digitaloutchannelcontroller = DigitalOutChannelControllerImpl(
                digital_out_channels, self.child_task_executor
            )
            self.set_feature_implementation(DigitalOutChannelControllerFeature, self.digitaloutchannelcontroller)
