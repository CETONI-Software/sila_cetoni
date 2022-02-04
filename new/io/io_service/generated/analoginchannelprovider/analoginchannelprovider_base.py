from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase


class AnalogInChannelProviderBase(FeatureImplementationBase, ABC):

    _Value_producer_queue: Queue[float]

    def __init__(self):
        """
        Allows to control one analog input channel of an I/O module
        """

        self._Value_producer_queue = Queue()

    @abstractmethod
    def get_NumberOfChannels(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        """
        The number of analog input channels.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of analog input channels.
        """
        pass

    def update_Value(self, Value: float, queue: Optional[Queue[float]] = None):
        """
        The value of the analog input channel.

        This method updates the observable property 'Value'.
        """
        if queue:
            queue.put(Value)
        else:
            self._Value_producer_queue.put(Value)

    def Value_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        The value of the analog input channel.

        This method is called when a client subscribes to the observable property 'Value'

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
