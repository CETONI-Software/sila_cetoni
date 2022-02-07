from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase


class DigitalInChannelProviderBase(FeatureImplementationBase, ABC):

    _State_producer_queue: Queue[State]

    def __init__(self):
        """
        Allows to control one digital input channel of an I/O module
        """

        self._State_producer_queue = Queue()

    @abstractmethod
    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        """
        The number of digital input channels.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of digital input channels.
        """
        pass

    def update_State(self, State: State, queue: Optional[Queue[State]] = None):
        """
        The state of the channel.

        This method updates the observable property 'State'.
        """
        if queue:
            queue.put(State)
        else:
            self._State_producer_queue.put(State)

    def State_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[State]]:
        """
        The state of the channel.

        This method is called when a client subscribes to the observable property 'State'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
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
