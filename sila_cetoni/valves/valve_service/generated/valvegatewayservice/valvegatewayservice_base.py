from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase


class ValveGatewayServiceBase(FeatureImplementationBase, ABC):

    """
    Provides means to access individual valves of a valve terminal
    """

    @abstractmethod
    def get_NumberOfValves(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        """
        The number of valves of a terminal

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The number of valves of a terminal
        """
        pass

    @abstractmethod
    def get_calls_affected_by_ValveIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        """
        Returns the fully qualified identifiers of all features, commands and properties affected by the
        SiLA Client Metadata 'Delay'.

        **Description of 'ValveIndex'**:
        The index of a single valve of a valve terminal. This value is 0-indexed, i.e. the first valve has index 0, the second one index 1 and so on.

        :return: Fully qualified identifiers of all features, commands and properties affected by the
            SiLA Client Metadata 'Delay'.
        """
        pass
