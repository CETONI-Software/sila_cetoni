from typing import Optional, Union
from uuid import UUID
from sila2.server import SilaServer

from device_drivers.balance import BalanceInterface

from .feature_implementations.balanceservice_impl import BalanceServiceImpl
from .generated.balanceservice import BalanceServiceFeature

class Server(SilaServer):
    def __init__(
        self,
        balance: BalanceInterface,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None):
        super().__init__(
            server_name=server_name or "BalanceService",
            server_type=server_type or "TestServer",
            server_description=server_description or "Allows to control a balance",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid
        )

        self.balanceservice = BalanceServiceImpl(balance, self.child_task_executor)

        self.set_feature_implementation(BalanceServiceFeature, self.balanceservice)
