from __future__ import annotations

from typing import Iterable, Optional

from continuousflowdosingservice_types import GenerateFlow_Responses, StopDosage_Responses
from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty

class ContinuousFlowDosingServiceClient:
    """

            Allows to continuously dose a specified fluid.
    The continuous flow mode is meant for dispensing volumes or generating flows and works only in one direction. That means using negative flow rates or negative volumes for aspiration is not possible.

    """

    MaxFlowRate: ClientObservableProperty[float]
    """
    The maximum value of the flow rate at which this pump can dose a fluid.
    """

    FlowRate: ClientObservableProperty[float]
    """
    The current value of the flow rate. It is 0 if the pump does not dose any fluid.
    """
    def StopDosage(self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None) -> StopDosage_Responses:
        """
        Stops a currently running dosage immediately.
        """
        ...
    def GenerateFlow(
        self, FlowRate: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, GenerateFlow_Responses]:
        """
        Generate a continuous flow with the given flow rate. Dosing continues until it gets stopped manually by calling StopDosage.

        """
        ...
