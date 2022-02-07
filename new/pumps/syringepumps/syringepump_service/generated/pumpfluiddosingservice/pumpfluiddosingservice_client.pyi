from __future__ import annotations

from typing import Iterable, Optional

from pumpfluiddosingservice_types import (
    DoseVolume_Responses,
    GenerateFlow_Responses,
    SetFillLevel_Responses,
    StopDosage_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty

class PumpFluidDosingServiceClient:
    """
    Allows to dose a specified fluid. There are commands for absolute dosing (SetFillLevel) and relative dosing (DoseVolume and GenerateFlow) available.

        The flow rate can be negative. In this case the pump aspirates the fluid instead of dispensing. The flow rate has to be a value between MaxFlowRate and MinFlowRate. If the value is not within this range (hence is invalid) a ValidationError will be thrown.
        At any time the property CurrentSyringeFillLevel can be queried to see how much fluid is left in the syringe. Similarly the property CurrentFlowRate can be queried to get the current flow rate at which the pump is dosing.
    """

    MaxSyringeFillLevel: ClientObservableProperty[float]
    """
    The maximum amount of fluid that the syringe can hold.
    """

    SyringeFillLevel: ClientObservableProperty[float]
    """
    The current amount of fluid left in the syringe.
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
    def SetFillLevel(
        self, FillLevel: float, FlowRate: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, SetFillLevel_Responses]:
        """
        Pumps fluid with the given flow rate until the requested fill level is reached.
                Depending on the requested fill level given in the FillLevel parameter this function may cause aspiration or dispension of fluid.
        """
        ...
    def DoseVolume(
        self, Volume: float, FlowRate: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, DoseVolume_Responses]:
        """
        Dose a certain amount of volume with the given flow rate.
        """
        ...
    def GenerateFlow(
        self, FlowRate: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, GenerateFlow_Responses]:
        """
        Generate a continuous flow with the given flow rate. Dosing continues until it gets stopped manually by calling StopDosage or until the pusher reached one of its limits.
        """
        ...
