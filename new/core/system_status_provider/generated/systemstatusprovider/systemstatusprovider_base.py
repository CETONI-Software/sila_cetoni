from __future__ import annotations

from abc import ABC
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase


class SystemStatusProviderBase(FeatureImplementationBase, ABC):

    _SystemState_producer_queue: Queue[str]

    def __init__(self):
        """
        Provides information about the overall system, e.g. if the system is operational or not
        """

        self._SystemState_producer_queue = Queue()

    def update_SystemState(self, SystemState: str):
        """
        The state of the system, e.g. if the system is operational or not. 'Operational' means that the system can process Commands and that all Property values are read from the device. 'Stopped' means that the system is unable to process Commands (i.e. all Execution will result in errors) and that Property values are not read from the device and might have outdated values.

        This method updates the observable property 'SystemState'.
        """
        self._SystemState_producer_queue.put(SystemState)

    def SystemState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The state of the system, e.g. if the system is operational or not. 'Operational' means that the system can process Commands and that all Property values are read from the device. 'Stopped' means that the system is unable to process Commands (i.e. all Execution will result in errors) and that Property values are not read from the device and might have outdated values.

        This method is called when a client subscribes to the observable property 'SystemState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass
