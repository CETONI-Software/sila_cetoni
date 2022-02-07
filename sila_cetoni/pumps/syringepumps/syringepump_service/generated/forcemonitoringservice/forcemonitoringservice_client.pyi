from __future__ import annotations

from typing import Iterable, Optional

from forcemonitoringservice_types import (
    ClearForceSafetyStop_Responses,
    DisableForceMonitoring_Responses,
    EnableForceMonitoring_Responses,
    SetForceLimit_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableProperty

from .forcemonitoringservice_types import Force

class ForceMonitoringServiceClient:
    """
    Functionality to control the force monitoring, read the force sensor and set a custom force limit for pump devices that support this functionality such as Nemesys S and Nemesys M.
    """

    ForceSensorValue: ClientObservableProperty[Force]
    """
    The currently measured force as read by the force sensor.
    """

    ForceLimit: ClientObservableProperty[Force]
    """
    The current force limit.
    """

    MaxDeviceForce: ClientObservableProperty[Force]
    """
    The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).
    """

    ForceMonitoringEnabled: ClientObservableProperty[bool]
    """
    Whether force monitoring is enabled.
    """

    ForceSafetyStopActive: ClientObservableProperty[bool]
    """
    Whether force safety stop is active.
    """

    def ClearForceSafetyStop(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClearForceSafetyStop_Responses:
        """
        Clear/acknowledge a force safety stop.
        """
        ...
    def EnableForceMonitoring(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> EnableForceMonitoring_Responses:
        """
        Enable the force monitoring.
        """
        ...
    def DisableForceMonitoring(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> DisableForceMonitoring_Responses:
        """
        Disable the force monitoring.
        """
        ...
    def SetForceLimit(
        self, ForceLimit: Force, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetForceLimit_Responses:
        """
        Set a custom limit.
        """
        ...
