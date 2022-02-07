from __future__ import annotations

from typing import Any, Iterable, Optional

from pumpunitcontroller_types import SetFlowUnit_Responses, SetVolumeUnit_Responses
from sila2.client import ClientMetadataInstance, ClientObservableProperty

from .pumpunitcontroller_types import VolumeUnit

class PumpUnitControllerClient:
    """
    Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.
    """

    FlowUnit: ClientObservableProperty[Any]
    """
    The currently used flow unit.
    """

    VolumeUnit: ClientObservableProperty[VolumeUnit]
    """
    The currently used volume unit.
    """

    def SetFlowUnit(
        self, FlowUnit: Any, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetFlowUnit_Responses:
        """
        Sets the flow unit for the pump. The flow unit defines the unit to be used for all flow values passed to or retrieved from the pump.
        """
        ...
    def SetVolumeUnit(
        self, VolumeUnit: VolumeUnit, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> SetVolumeUnit_Responses:
        """
        Sets the default volume unit. The volume unit defines the unit to be used for all volume values passed to or retrieved from the pump.
        """
        ...
