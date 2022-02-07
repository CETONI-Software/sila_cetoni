from typing import List, Optional, Union
from uuid import UUID
from sila2.server import SilaServer

from qmixsdk.qmixcontroller import ControllerChannel

from .feature_implementations.controlloopservice_impl import ControlLoopServiceImpl
from .generated.controlloopservice import ControlLoopServiceFeature


class Server(SilaServer):
    def __init__(
        self,
        controller_channels: List[ControllerChannel],
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None):
        super().__init__(
            server_name=server_name or "Control Loop Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI reaction modules",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid
        )

        self.controlloopservice = ControlLoopServiceImpl(controller_channels, self.child_task_executor)

        self.set_feature_implementation(ControlLoopServiceFeature, self.controlloopservice)
