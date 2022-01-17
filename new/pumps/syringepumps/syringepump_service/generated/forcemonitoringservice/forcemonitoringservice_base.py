from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .forcemonitoringservice_types import (
    ClearForceSafetyStop_Responses,
    DisableForceMonitoring_Responses,
    EnableForceMonitoring_Responses,
    Force,
    SetForceLimit_Responses,
)


class ForceMonitoringServiceBase(FeatureImplementationBase, ABC):

    _ForceSensorValue_producer_queue: Queue[Force]

    _ForceLimit_producer_queue: Queue[Force]

    _MaxDeviceForce_producer_queue: Queue[Force]

    _ForceMonitoringEnabled_producer_queue: Queue[bool]

    _ForceSafetyStopActive_producer_queue: Queue[bool]

    def __init__(self):
        """
        Functionality to control the force monitoring, read the force sensor and set a custom force limit for pump devices that support this functionality such as Nemesys S and Nemesys M.
        """

        self._ForceSensorValue_producer_queue = Queue()

        self._ForceLimit_producer_queue = Queue()

        self._MaxDeviceForce_producer_queue = Queue()

        self._ForceMonitoringEnabled_producer_queue = Queue()

        self._ForceSafetyStopActive_producer_queue = Queue()

    def update_ForceSensorValue(self, ForceSensorValue: Force):
        """
        The currently measured force as read by the force sensor.

        This method updates the observable property 'ForceSensorValue'.
        """
        self._ForceSensorValue_producer_queue.put(ForceSensorValue)

    def ForceSensorValue_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The currently measured force as read by the force sensor.

        This method is called when a client subscribes to the observable property 'ForceSensorValue'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_ForceLimit(self, ForceLimit: Force):
        """
        The current force limit.

        This method updates the observable property 'ForceLimit'.
        """
        self._ForceLimit_producer_queue.put(ForceLimit)

    def ForceLimit_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The current force limit.

        This method is called when a client subscribes to the observable property 'ForceLimit'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_MaxDeviceForce(self, MaxDeviceForce: Force):
        """
        The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).

        This method updates the observable property 'MaxDeviceForce'.
        """
        self._MaxDeviceForce_producer_queue.put(MaxDeviceForce)

    def MaxDeviceForce_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The maximum device force (i.e. the maximum force the pump hardware can take in continuous operation).

        This method is called when a client subscribes to the observable property 'MaxDeviceForce'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_ForceMonitoringEnabled(self, ForceMonitoringEnabled: bool):
        """
        Whether force monitoring is enabled.

        This method updates the observable property 'ForceMonitoringEnabled'.
        """
        self._ForceMonitoringEnabled_producer_queue.put(ForceMonitoringEnabled)

    def ForceMonitoringEnabled_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Whether force monitoring is enabled.

        This method is called when a client subscribes to the observable property 'ForceMonitoringEnabled'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    def update_ForceSafetyStopActive(self, ForceSafetyStopActive: bool):
        """
        Whether force safety stop is active.

        This method updates the observable property 'ForceSafetyStopActive'.
        """
        self._ForceSafetyStopActive_producer_queue.put(ForceSafetyStopActive)

    def ForceSafetyStopActive_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Whether force safety stop is active.

        This method is called when a client subscribes to the observable property 'ForceSafetyStopActive'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    @abstractmethod
    def ClearForceSafetyStop(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> ClearForceSafetyStop_Responses:
        """
        Clear/acknowledge a force safety stop.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def EnableForceMonitoring(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> EnableForceMonitoring_Responses:
        """
        Enable the force monitoring.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def DisableForceMonitoring(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> DisableForceMonitoring_Responses:
        """
        Disable the force monitoring.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetForceLimit(
        self, ForceLimit: Force, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetForceLimit_Responses:
        """
        Set a custom limit.


        :param ForceLimit: The force limit to set. If higher than MaxDeviceForce, MaxDeviceForce will be used instead.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
