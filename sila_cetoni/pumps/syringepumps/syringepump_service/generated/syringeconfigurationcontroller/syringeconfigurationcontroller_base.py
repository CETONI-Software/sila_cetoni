from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .syringeconfigurationcontroller_types import SetSyringeParameters_Responses


class SyringeConfigurationControllerBase(FeatureImplementationBase, ABC):

    _InnerDiameter_producer_queue: Queue[float]

    _MaxPistonStroke_producer_queue: Queue[float]

    def __init__(self):
        """
        Provides syringe pump specific functions for configuration (i.e. the configuration of the syringe itself).
        """

        self._InnerDiameter_producer_queue = Queue()

        self._MaxPistonStroke_producer_queue = Queue()

    def update_InnerDiameter(self, InnerDiameter: float, queue: Optional[Queue[float]] = None):
        """
        Inner diameter of the syringe tube in millimetres.

        This method updates the observable property 'InnerDiameter'.
        """
        if queue is None:
            queue = self._InnerDiameter_producer_queue
        queue.put(InnerDiameter)

    def InnerDiameter_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        Inner diameter of the syringe tube in millimetres.

        This method is called when a client subscribes to the observable property 'InnerDiameter'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    def update_MaxPistonStroke(self, MaxPistonStroke: float, queue: Optional[Queue[float]] = None):
        """
        The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        This method updates the observable property 'MaxPistonStroke'.
        """
        if queue is None:
            queue = self._MaxPistonStroke_producer_queue
        queue.put(MaxPistonStroke)

    def MaxPistonStroke_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[float]]:
        """
        The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        This method is called when a client subscribes to the observable property 'MaxPistonStroke'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    @abstractmethod
    def SetSyringeParameters(
        self, InnerDiameter: float, MaxPistonStroke: float, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> SetSyringeParameters_Responses:
        """
        Set syringe parameters.
            If you change the syringe in one device, you need to setup the new syringe parameters to get proper conversion of flow rate und volume units.


        :param InnerDiameter: Inner diameter of the syringe tube in millimetres.

        :param MaxPistonStroke: The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.

        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
