from __future__ import annotations

from typing import Iterable, Optional

from pumpdrivecontrolservice_types import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializePumpDrive_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty

class PumpDriveControlServiceClient:
    """

    Functionality to control and maintain the drive that drives the pump.
    Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump drive's current state (i.e. enabled/disabled).
    The initialization has to be successful in order for the pump to work correctly and dose fluids. If the initialization fails, the DefinedExecutionError InitializationFailed is thrown.

    """

    PumpDriveState: ClientObservableProperty[str]
    """
    The current state of the pump. This is either 'Enabled' or 'Disabled'. Only if the sate is 'Enabled', the pump can dose fluids.
    """

    FaultState: ClientObservableProperty[bool]
    """
    Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling EnablePumpDrive.
    """
    def EnablePumpDrive(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> EnablePumpDrive_Responses:
        """
        Set the pump into enabled state.
        """
        ...
    def DisablePumpDrive(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> DisablePumpDrive_Responses:
        """
        Set the pump into disabled state.
        """
        ...
    def InitializePumpDrive(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, InitializePumpDrive_Responses]:
        """
        Initialize the pump drive (e.g. by executing a reference move).
        """
        ...
