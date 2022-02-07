from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

if TYPE_CHECKING:

    from .continuousflowconfigurationservice import ContinuousFlowConfigurationServiceClient
    from .continuousflowdosingservice import ContinuousFlowDosingServiceClient
    from .continuousflowinitializationcontroller import ContinuousFlowInitializationControllerClient


class Client(SilaClient):

    ContinuousFlowConfigurationService: ContinuousFlowConfigurationServiceClient

    ContinuousFlowDosingService: ContinuousFlowDosingServiceClient

    ContinuousFlowInitializationController: ContinuousFlowInitializationControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
