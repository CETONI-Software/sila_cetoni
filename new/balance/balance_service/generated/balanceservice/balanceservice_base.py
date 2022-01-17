from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .balanceservice_types import Tare_Responses


class BalanceServiceBase(FeatureImplementationBase, ABC):

    _Value_producer_queue: Queue[float]

    def __init__(self):
        """
        Provides an interface to a balance to read its current value and tare the balance if necessary
        """

        self._Value_producer_queue = Queue()

    def update_Value(self, Value: float):
        """
        The current value

        This method updates the observable property 'Value'.
        """
        self._Value_producer_queue.put(Value)

    def Value_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        The current value

        This method is called when a client subscribes to the observable property 'Value'

        :param metadata: The SiLA Client Metadata attached to the call
        :return:
        """
        pass

    @abstractmethod
    def Tare(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Tare_Responses:
        """
        Tare the balance


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
