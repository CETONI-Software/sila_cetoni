from typing import List, Optional, Union
from uuid import UUID

from ...core.system_status_provider.server import Server as SystemStatusProviderServer

from qmixsdk.qmixvalve import Valve

from .feature_implementations.valvegatewayservice_impl import ValveGatewayServiceImpl
from .feature_implementations.valvepositioncontroller_impl import ValvePositionControllerImpl
from .generated.valvegatewayservice import ValveGatewayServiceFeature
from .generated.valvepositioncontroller import ValvePositionControllerFeature


class Server(SystemStatusProviderServer):
    def __init__(
        self,
        valves: List[Valve] = [],
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        super().__init__(
            server_name=server_name or "Valve Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI valve modules",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )
        if len(valves) == 1:
            # a single valve can be controlled directly without the gateway
            self.valvepositioncontroller = ValvePositionControllerImpl(
                valve=valves[0], executor=self.child_task_executor
            )
            self.set_feature_implementation(ValvePositionControllerFeature, self.valvepositioncontroller)
        else:
            self.valvegatewayservice = ValveGatewayServiceImpl(valves)
            self.valvepositioncontroller = ValvePositionControllerImpl(
                gateway=self.valvegatewayservice, executor=self.child_task_executor
            )
            self.set_feature_implementation(ValveGatewayServiceFeature, self.valvegatewayservice)
            self.set_feature_implementation(ValvePositionControllerFeature, self.valvepositioncontroller)
