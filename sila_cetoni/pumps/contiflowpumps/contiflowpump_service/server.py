from typing import Optional, Union
from uuid import UUID

from qmixsdk.qmixpump import ContiFlowPump

from ...syringepumps.syringepump_service.server import Server as SyringePumpServer
from .feature_implementations.continuousflowconfigurationservice_impl import ContinuousFlowConfigurationServiceImpl
from .feature_implementations.continuousflowdosingservice_impl import ContinuousFlowDosingServiceImpl
from .feature_implementations.continuousflowinitializationcontroller_impl import (
    ContinuousFlowInitializationControllerImpl,
)
from .generated.continuousflowconfigurationservice import ContinuousFlowConfigurationServiceFeature
from .generated.continuousflowdosingservice import ContinuousFlowDosingServiceFeature
from .generated.continuousflowinitializationcontroller import ContinuousFlowInitializationControllerFeature


class Server(SyringePumpServer):
    def __init__(
        self,
        pump: ContiFlowPump,
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        super().__init__(
            pump,
            server_name=server_name or "Continuous Flow Service",
            server_type=server_type or "TestServer",
            server_description=server_description or "The SiLA 2 driver for CETONI continuous flow syringe pumps",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        self.continuousflowconfigurationservice = ContinuousFlowConfigurationServiceImpl(pump, self.child_task_executor)
        self.continuousflowdosingservice = ContinuousFlowDosingServiceImpl(pump, self.child_task_executor)
        self.continuousflowinitializationcontroller = ContinuousFlowInitializationControllerImpl(
            pump, self.child_task_executor
        )

        self.set_feature_implementation(
            ContinuousFlowConfigurationServiceFeature, self.continuousflowconfigurationservice
        )
        self.set_feature_implementation(ContinuousFlowDosingServiceFeature, self.continuousflowdosingservice)
        self.set_feature_implementation(
            ContinuousFlowInitializationControllerFeature, self.continuousflowinitializationcontroller
        )
