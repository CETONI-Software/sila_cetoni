from __future__ import annotations

from typing import Iterable, Optional

from sila2.client import ClientMetadataInstance, ClientObservableProperty
from syringeconfigurationcontroller_types import SetSyringeParameters_Responses

class SyringeConfigurationControllerClient:
    """
    Provides syringe pump specific functions for configuration (i.e. the configuration of the syringe itself).
    """

    InnerDiameter: ClientObservableProperty[float]
    """
    Inner diameter of the syringe tube in millimetres.
    """

    MaxPistonStroke: ClientObservableProperty[float]
    """
    The maximum piston stroke defines the maximum position the piston can be moved to before it slips out of the syringe tube. The maximum piston stroke limits the maximum travel range of the syringe pump pusher.
    """

    def SetSyringeParameters(
        self,
        InnerDiameter: float,
        MaxPistonStroke: float,
        *,
        metadata: Optional[Iterable[ClientMetadataInstance]] = None,
    ) -> SetSyringeParameters_Responses:
        """
        Set syringe parameters.
            If you change the syringe in one device, you need to setup the new syringe parameters to get proper conversion of flow rate und volume units.
        """
        ...
