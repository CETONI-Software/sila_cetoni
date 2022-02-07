from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .pumpdrivecontrolservice_types import (
    DisablePumpDrive_Responses,
    EnablePumpDrive_Responses,
    InitializePumpDrive_Responses,
    RestoreDrivePositionCounter_Responses,
)


class PumpDriveControlServiceBase(FeatureImplementationBase, ABC):

    _PumpDriveState_producer_queue: Queue[str]

    _FaultState_producer_queue: Queue[bool]

    _DrivePositionCounter_producer_queue: Queue[int]

    def __init__(self):
        """
        Functionality to control and maintain the drive that drives the pump.
        Allows to initialize a pump (e.g. by executing a reference move) and obtain status information about the pump drive's current state (i.e. enabled/disabled).
        The initialization has to be successful in order for the pump to work correctly and dose fluids. If the initialization fails, the DefinedExecutionError InitializationFailed is thrown.
        """

        self._PumpDriveState_producer_queue = Queue()

        self._FaultState_producer_queue = Queue()

        self._DrivePositionCounter_producer_queue = Queue()

    def update_PumpDriveState(self, PumpDriveState: str, queue: Optional[Queue[str]] = None):
        """
        The current state of the pump. This is either 'Enabled' or 'Disabled'. Only if the sate is 'Enabled', the pump can dose fluids.

        This method updates the observable property 'PumpDriveState'.
        """
        if queue is None:
            queue = self._PumpDriveState_producer_queue
        queue.put(PumpDriveState)

    def PumpDriveState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[str]]:
        """
        The current state of the pump. This is either 'Enabled' or 'Disabled'. Only if the sate is 'Enabled', the pump can dose fluids.

        This method is called when a client subscribes to the observable property 'PumpDriveState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_FaultState(self, FaultState: bool, queue: Optional[Queue[bool]] = None):
        """
        Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling EnablePumpDrive.

        This method updates the observable property 'FaultState'.
        """
        if queue is None:
            queue = self._FaultState_producer_queue
        queue.put(FaultState)

    def FaultState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[bool]]:
        """
        Returns if the pump is in fault state. If the value is true (i.e. the pump is in fault state), it can be cleared by calling EnablePumpDrive.

        This method is called when a client subscribes to the observable property 'FaultState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_DrivePositionCounter(self, DrivePositionCounter: int, queue: Optional[Queue[int]] = None):
        """
        Returns the value of the internal drive position counter. You can query this value and store it persistently somewhere before shutting down the device and restore it later using the RestoreDrivePositionCounter Command.

        This method updates the observable property 'DrivePositionCounter'.
        """
        if queue is None:
            queue = self._DrivePositionCounter_producer_queue
        queue.put(DrivePositionCounter)

    def DrivePositionCounter_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[int]]:
        """
        Returns the value of the internal drive position counter. You can query this value and store it persistently somewhere before shutting down the device and restore it later using the RestoreDrivePositionCounter Command.

        This method is called when a client subscribes to the observable property 'DrivePositionCounter'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
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
    def RestoreDrivePositionCounter(
        self, DrivePositionCounterValue: int, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> RestoreDrivePositionCounter_Responses:
        """
        Restore the internal hardware position counter value of the pump drive. This function is not required and not supported for devices that have an absolute encoder such as the new Nemesys 4 devices Nemesys S and Nemesys M.


        :param DrivePositionCounterValue: The position counter value to restore

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
