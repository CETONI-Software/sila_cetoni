import logging
from typing import Optional, Union
from uuid import UUID

from application.system import ApplicationSystem
from ...core.system_status_provider.server import Server as SystemStatusProviderServer

from .feature_implementations.batteryprovider_impl import BatteryProviderImpl
from .generated.batteryprovider import BatteryProviderFeature


class Server(SystemStatusProviderServer):
    def __init__(
        self,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None):
        super().__init__(
            server_name=server_name or "BatteryProvider",
            server_type=server_type or "TestServer",
            server_description=server_description or "A device that is powered by a battery",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid
        )

        if not ApplicationSystem().device_config.has_battery:
            logging.debug("This device does not have a battery")
            return

        self.batteryprovider = BatteryProviderImpl(self.child_task_executor)

        self.set_feature_implementation(BatteryProviderFeature, self.batteryprovider)
