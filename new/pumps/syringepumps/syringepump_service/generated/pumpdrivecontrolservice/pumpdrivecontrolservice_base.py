from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .pumpdrivecontrolservice_types import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializePumpDrive_Responses,
)


class PumpDriveControlServiceBase(FeatureImplementationBase, ABC):

    _PumpDriveState_producer_queue: Queue[str]

    _FaultState_producer_queue: Queue[bool]

    def __init__(self):
        """

        Functionality to control and maintain the drive that drives the pump.
        Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump drive's current state (i.e. enabled/disabled).
        The initialization has to be successful in order for the pump to work correctly and dose fluids. If the initialization fails, the DefinedExecutionError InitializationFailed is thrown.

        """

        self._PumpDriveState_producer_queue = Queue()

        self._FaultState_producer_queue = Queue()

    def update_PumpDriveState(self, PumpDriveState: str):
        """
        The current state of the pump. This is either 'Enabled' or 'Disabled'. Only if the sate is 'Enabled', the pump can dose fluids.

        This method updates the observable property 'PumpDriveState'.
        """
        self._PumpDriveState_producer_queue.put(PumpDriveState)

    def PumpDriveState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The current state of the pump. This is either 'Enabled' or 'Disabled'. Only if the sate is 'Enabled', the pump can dose fluids.

        This method is called when a client subscribes to the observable property 'PumpDriveState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_FaultState(self, FaultState: bool):
        """
        Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling EnablePumpDrive.

        This method updates the observable property 'FaultState'.
        """
        self._FaultState_producer_queue.put(FaultState)

    def FaultState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling EnablePumpDrive.

        This method is called when a client subscribes to the observable property 'FaultState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    @abstractmethod
    def EnablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> EnablePumpDrive_Responses:
        """
        Set the pump into enabled state.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def DisablePumpDrive(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> DisablePumpDrive_Responses:
        """
        Set the pump into disabled state.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def InitializePumpDrive(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> InitializePumpDrive_Responses:
        """
        Initialize the pump drive (e.g. by executing a reference move).


        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass
