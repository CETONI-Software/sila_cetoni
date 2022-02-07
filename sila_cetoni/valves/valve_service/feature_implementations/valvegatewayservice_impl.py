from __future__ import annotations
import logging
from queue import Queue

from typing import Any, Dict, List, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.framework.errors.framework_error import FrameworkError, FrameworkErrorType

from qmixsdk.qmixvalve import Valve

from ..generated.valvegatewayservice import (
    ValveGatewayServiceBase,
    ValveGatewayServiceFeature,
    InvalidValveIndex,
)
from ..generated.valvepositioncontroller import ValvePositionControllerFeature


class ValveGatewayServiceImpl(ValveGatewayServiceBase):
    __valves: List[Valve]
    __valve_index_identifier: FullyQualifiedIdentifier

    def __init__(self, valves: List[Valve]) -> None:
        super().__init__()
        self.__valves = valves
        self.__valve_index_identifier = ValveGatewayServiceFeature["ValveIndex"].fully_qualified_identifier

    def get_NumberOfValves(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> int:
        return len(self.__valves)

    def get_calls_affected_by_ValveIndex(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [ValvePositionControllerFeature]

    def get_valve(self, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Valve:
        """
        Get the valve that is identified by the valve index given in `metadata`

        :param metdata: The metadata of the call. It should contain the requested valve index
        :return: A valid `Valve` object if the valve can be identified, otherwise a FrameworkError will be raised
        """

        valve_index: int = metadata.pop(self.__valve_index_identifier)
        logging.debug(f"Requested valve: {valve_index}")

        try:
            return self.__valves[valve_index]
        except IndexError:
            raise InvalidValveIndex(
                message=f"The sent Valve Index ({valve_index}) is invalid! The index has to be between 0 and {len(self.__valves) - 1}."
            )

    @property
    def valves(self) -> List[Valve]:
        return self.__valves

    @property
    def valve_index_identifier(self) -> FullyQualifiedIdentifier:
        return self.__valve_index_identifier
