from __future__ import annotations

from sila2.client import ClientObservableProperty

class BatteryProviderClient:
    """
    Provides information on the battery state
    """

    BatteryVoltage: ClientObservableProperty[float]
    """
    The current voltage of the battery
    """
