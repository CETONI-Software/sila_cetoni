from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .controlloopservice_types import RunControlLoop_Responses, StopControlLoop_Responses, WriteSetPoint_Responses


class ControlLoopServiceBase(FeatureImplementationBase, ABC):

    _ControllerValue_producer_queue: Queue[float]

    _SetPointValue_producer_queue: Queue[float]

    def __init__(self):
        """
        Allows to control a Qmix Device with a Control Loop
        """

        self._ControllerValue_producer_queue = Queue()

        self._SetPointValue_producer_queue = Queue()

    @abstractmethod
    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        """
        The number of controller channels.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of controller channels.
        """
        pass

    def update_ControllerValue(self, ControllerValue: float, queue: Optional[Queue[float]] = None):
        """
        The actual value from the Device

        This method updates the observable property 'ControllerValue'.
        """
        if queue:
            queue.put(ControllerValue)
        else:
            self._ControllerValue_producer_queue.put(ControllerValue)

    def ControllerValue_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[float]]:
        """
        The actual value from the Device

        This method is called when a client subscribes to the observable property 'ControllerValue'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    def update_SetPointValue(self, SetPointValue: float, queue: Optional[Queue[float]] = None):
        """
        The current SetPoint value of the Device

        This method updates the observable property 'SetPointValue'.
        """
        if queue:
            queue.put(SetPointValue)
        else:
            self._SetPointValue_producer_queue.put(SetPointValue)

    def SetPointValue_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        The current SetPoint value of the Device

        This method is called when a client subscribes to the observable property 'SetPointValue'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    @abstractmethod
    def WriteSetPoint(
        self, SetPointValue: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> WriteSetPoint_Responses:
        """
        Write a Set Point value to the Controller Device


        :param SetPointValue: The Set Point value to write

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def StopControlLoop(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopControlLoop_Responses:
        """
        Stops the Control Loop (has no effect, if no Loop is currently running)


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def RunControlLoop(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any], instance: ObservableCommandInstance
    ) -> RunControlLoop_Responses:
        """
        Run the Control Loop


        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def get_calls_affected_by_ChannelIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        """
        Returns the fully qualified identifiers of all features, commands and properties affected by the
        SiLA Client Metadata 'Delay'.

        **Description of 'ChannelIndex'**:
        The index of the channel that should be used. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.

        :return: Fully qualified identifiers of all features, commands and properties affected by the
            SiLA Client Metadata 'Delay'.
        """
        pass
