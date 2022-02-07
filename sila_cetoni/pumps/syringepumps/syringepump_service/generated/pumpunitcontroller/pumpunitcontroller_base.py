from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .pumpunitcontroller_types import SetFlowUnit_Responses, SetVolumeUnit_Responses, VolumeUnit


class PumpUnitControllerBase(FeatureImplementationBase, ABC):

    _FlowUnit_producer_queue: Queue[Any]

    _VolumeUnit_producer_queue: Queue[VolumeUnit]

    def __init__(self):
        """
        Allows to control the currently used units for passing and retrieving flow rates and volumes to and from a pump.
        """

        self._FlowUnit_producer_queue = Queue()

        self._VolumeUnit_producer_queue = Queue()

    def update_FlowUnit(self, FlowUnit: Any, queue: Optional[Queue[Any]] = None):
        """
        The currently used flow unit.

        This method updates the observable property 'FlowUnit'.
        """
        if queue is None:
            queue = self._FlowUnit_producer_queue
        queue.put(FlowUnit)

    def FlowUnit_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[Any]]:
        """
        The currently used flow unit.

        This method is called when a client subscribes to the observable property 'FlowUnit'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_VolumeUnit(self, VolumeUnit: VolumeUnit, queue: Optional[Queue[VolumeUnit]] = None):
        """
        The currently used volume unit.

        This method updates the observable property 'VolumeUnit'.
        """
        if queue is None:
            queue = self._VolumeUnit_producer_queue
        queue.put(VolumeUnit)

    def VolumeUnit_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[VolumeUnit]]:
        """
        The currently used volume unit.

        This method is called when a client subscribes to the observable property 'VolumeUnit'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    @abstractmethod
    def SetFlowUnit(self, FlowUnit: Any, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> SetFlowUnit_Responses:
        """
        Sets the flow unit for the pump. The flow unit defines the unit to be used for all flow values passed to or retrieved from the pump.


        :param FlowUnit: The flow unit to be set.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def SetVolumeUnit(
        self, VolumeUnit: VolumeUnit, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetVolumeUnit_Responses:
        """
        Sets the default volume unit. The volume unit defines the unit to be used for all volume values passed to or retrieved from the pump.


        :param VolumeUnit: The volume unit for the flow rate.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
