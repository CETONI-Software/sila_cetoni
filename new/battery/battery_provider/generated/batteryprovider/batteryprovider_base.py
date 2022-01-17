from __future__ import annotations

from abc import ABC
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase


class BatteryProviderBase(FeatureImplementationBase, ABC):

    _BatteryVoltage_producer_queue: Queue[float]

    def __init__(self):
        """
        Provides information on the battery state
        """

        self._BatteryVoltage_producer_queue = Queue()

    def update_BatteryVoltage(self, BatteryVoltage: float):
        """
        The current voltage of the battery

        This method updates the observable property 'BatteryVoltage'.
        """
        self._BatteryVoltage_producer_queue.put(BatteryVoltage)

    def BatteryVoltage_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The current voltage of the battery

        This method is called when a client subscribes to the observable property 'BatteryVoltage'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass
