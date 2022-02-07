from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .valvepositioncontroller_types import SwitchToPosition_Responses, TogglePosition_Responses


class ValvePositionControllerBase(FeatureImplementationBase, ABC):

    _Position_producer_queue: Queue[int]

    def __init__(self):
        """
        Allows to specify a certain logical position for a valve. The Position property can be querried at any time to obtain the current valve position.
        """

        self._Position_producer_queue = Queue()

    @abstractmethod
    def get_NumberOfPositions(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        """
        The number of the valve positions available.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of the valve positions available.
        """
        pass

    def update_Position(self, Position: int, queue: Optional[Queue[int]] = None):
        """
        The current logical valve position. This is a value between 0 and NumberOfPositions - 1.

        This method updates the observable property 'Position'.
        """
        if queue:
            queue.put(Position)
        else:
            self._Position_producer_queue.put(Position)

    def Position_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[int]]:
        """
        The current logical valve position. This is a value between 0 and NumberOfPositions - 1.

        This method is called when a client subscribes to the observable property 'Position'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    @abstractmethod
    def SwitchToPosition(
        self, Position: int, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SwitchToPosition_Responses:
        """
        Switches the valve to the specified position. The given position has to be less than the NumberOfPositions or else a ValidationError is thrown.


        :param Position: The target position that the valve should be switched to.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def TogglePosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> TogglePosition_Responses:
        """
        This command only applies for 2-way valves to toggle between its two different positions. If the command is called for any other valve type a ValveNotToggleable error is thrown.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
