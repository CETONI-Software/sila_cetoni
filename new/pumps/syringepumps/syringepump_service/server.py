from typing import List, Optional, Union
from uuid import UUID

from ....io.io_service.server import Server as IOServer

from qmixsdk.qmixpump import ContiFlowPump, Pump
from qmixsdk.qmixvalve import Valve

from .feature_implementations.forcemonitoringservice_impl import ForceMonitoringServiceImpl
from .feature_implementations.pumpdrivecontrolservice_impl import PumpDriveControlServiceImpl
from .feature_implementations.pumpfluiddosingservice_impl import PumpFluidDosingServiceImpl
from .feature_implementations.pumpunitcontroller_impl import PumpUnitControllerImpl
from .feature_implementations.syringeconfigurationcontroller_impl import SyringeConfigurationControllerImpl
from ....valves.valve_service.feature_implementations.valvepositioncontroller_impl import ValvePositionControllerImpl
from .generated.forcemonitoringservice import ForceMonitoringServiceFeature
from .generated.pumpdrivecontrolservice import PumpDriveControlServiceFeature
from .generated.pumpfluiddosingservice import PumpFluidDosingServiceFeature
from .generated.pumpunitcontroller import PumpUnitControllerFeature
from .generated.syringeconfigurationcontroller import SyringeConfigurationControllerFeature
from ....valves.valve_service.generated.valvepositioncontroller import ValvePositionControllerFeature

class Server(IOServer):
    def __init__(
        self,
        pump: Union[Pump, ContiFlowPump],
        valve: Optional[Valve] = None,
        io_channels: List = [],
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None):
        super().__init__(
            io_channels,
            server_name=server_name or "Syringe Pump Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI syringe pumps",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid
        )

        # common features
        self.pumpdrivecontrolservice = PumpDriveControlServiceImpl(pump, self.child_task_executor)
        self.pumpunitcontroller = PumpUnitControllerImpl(pump, self.child_task_executor)
        self.set_feature_implementation(PumpDriveControlServiceFeature, self.pumpdrivecontrolservice)
        self.set_feature_implementation(PumpUnitControllerFeature, self.pumpunitcontroller)

        if not isinstance(pump, ContiFlowPump):
            # features for real syringe pumps only
            self.syringeconfigurationcontroller = SyringeConfigurationControllerImpl(pump, self.child_task_executor)
            self.set_feature_implementation(SyringeConfigurationControllerFeature, self.syringeconfigurationcontroller)

            if pump.has_force_monitoring():
                self.forcemonitoringservice = ForceMonitoringServiceImpl(pump, self.child_task_executor)
                self.set_feature_implementation(ForceMonitoringServiceFeature, self.forcemonitoringservice)

            self.pumpfluiddosingservice = PumpFluidDosingServiceImpl(pump, self.child_task_executor)
            self.set_feature_implementation(PumpFluidDosingServiceFeature, self.pumpfluiddosingservice)

            if valve:
                self.valvepositioncontroller = ValvePositionControllerImpl(valve=valve, executor=self.child_task_executor)
                self.set_feature_implementation(ValvePositionControllerFeature, self.valvepositioncontroller)

        # TODO shutdown controller
