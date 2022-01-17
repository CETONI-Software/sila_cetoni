from __future__ import annotations

from typing import Iterable, Optional

from sila2.client import ClientMetadataInstance, ClientObservableProperty, ClientUnobservableProperty
from valvepositioncontroller_types import SwitchToPosition_Responses, TogglePosition_Responses

class ValvePositionControllerClient:
    """
    Allows to specify a certain logical position for a valve. The Position property can be querried at any time to obtain the current valve position.
    """

    NumberOfPositions: ClientUnobservableProperty[int]
    """
    The number of the valve positions available.
    """

    Position: ClientObservableProperty[int]
    """
    The current logical valve position. This is a value between 0 and NumberOfPositions - 1.
    """
    def SwitchToPosition(
        self, Position: int, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SwitchToPosition_Responses:
        """
        Switches the valve to the specified position. The given position has to be less than the NumberOfPositions or else a ValidationError is thrown.
        """
        ...
    def TogglePosition(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> TogglePosition_Responses:
        """
        This command only applies for 2-way valves to toggle between its two different positions. If the command is called for any other valve type a ValveNotToggleable error is thrown.
        """
        ...
