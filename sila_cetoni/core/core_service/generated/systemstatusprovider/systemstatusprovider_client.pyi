from __future__ import annotations

from sila2.client import ClientObservableProperty

class SystemStatusProviderClient:
    """
    Provides information about the overall system, e.g. if the system is operational or not
    """

    SystemState: ClientObservableProperty[str]
    """
    The state of the system, e.g. if the system is operational or not. 'Operational' means that the system can process Commands and that all Property values are read from the device. 'Stopped' means that the system is unable to process Commands (i.e. all Execution will result in errors) and that Property values are not read from the device and might have outdated values.
    """
