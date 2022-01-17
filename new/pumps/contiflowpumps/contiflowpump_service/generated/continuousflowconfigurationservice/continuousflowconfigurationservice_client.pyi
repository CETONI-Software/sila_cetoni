from __future__ import annotations

from typing import Iterable, Optional

from continuousflowconfigurationservice_types import (
    SetCrossFlowDuration_Responses,
    SetOverlapDuration_Responses,
    SetRefillFlowRate_Responses,
    SetSwitchingMode_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableProperty

class ContinuousFlowConfigurationServiceClient:
    """
    Allows to configure the parameters of a continuous flow pump.
    """

    SwitchingMode: ClientObservableProperty[str]
    """
    Get the switching mode for syringe pump switchover if one syringe pump runs empty.
    """

    MaxRefillFlowRate: ClientObservableProperty[float]
    """
    Get the maximum possible refill flow rate for the continuous flow pump.
    """

    RefillFlowRate: ClientObservableProperty[float]
    """
    Get the refill flow rate for the continuous flow pump.
    """

    MinFlowRate: ClientObservableProperty[float]
    """
    Get the minimum flow rate that is theoretically possible with the continuous flow pump.
    """

    CrossFlowDuration: ClientObservableProperty[float]
    """
    Get the cross flow duration for the continuous flow pump.
    """

    OverlapDuration: ClientObservableProperty[float]
    """
    Get the overlap duration for the continuous flow pump.
    """
    def SetSwitchingMode(
        self, SwitchingMode: str, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetSwitchingMode_Responses:
        """
        Sets the switching mode for syringe pump switchover if one syringe pump runs empty.
        """
        ...
    def SetRefillFlowRate(
        self, RefillFlowRate: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetRefillFlowRate_Responses:
        """
        Set the refill flow rate for the continuous flow pump. The refill flow speed limits the maximum flow that is possible with a contiflow pump.
        """
        ...
    def SetCrossFlowDuration(
        self, CrossFlowDuration: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetCrossFlowDuration_Responses:
        """
        Set the cross flow duration for the continuous flow pump. The cross flow duration is the time the pump running empty decelerates while the filled pump accelerates.
        """
        ...
    def SetOverlapDuration(
        self, OverlapDuration: float, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetOverlapDuration_Responses:
        """
        Set the overlap duration for the continuous flow pump. The overlap duration is a time the refilled pump will start earlier than the empty pump stops. You can use this time to ensure that the system is already pressurized when switching over.
        """
        ...
