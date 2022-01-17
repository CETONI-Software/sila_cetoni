from typing import Optional, Union
from uuid import UUID
from sila2.server import SilaServer

from .feature_implementations.systemstatusprovider_impl import SystemStatusProviderImpl
from .generated.systemstatusprovider import SystemStatusProviderFeature


class Server(SilaServer):
    def __init__(
        self,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None):
        super().__init__(
            server_name=server_name or "SystemStatusProvider",
            server_type=server_type or "TestServer",
            server_description=server_description or "Provides status information about the overall system",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
            max_child_task_workers=1000,
            max_grpc_workers=1000,
        )

        self.systemstatusprovider = SystemStatusProviderImpl(self.child_task_executor)

        self.set_feature_implementation(SystemStatusProviderFeature, self.systemstatusprovider)
