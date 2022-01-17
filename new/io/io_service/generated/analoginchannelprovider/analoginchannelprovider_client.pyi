from __future__ import annotations

from sila2.client import ClientMetadata, ClientObservableProperty, ClientUnobservableProperty

class AnalogInChannelProviderClient:
    """
    Allows to control one analog input channel of an I/O module
    """

    NumberOfChannels: ClientUnobservableProperty[int]
    """
    The number of analog input channels.
    """

    Value: ClientObservableProperty[float]
    """
    The value of the analog input channel.
    """

    ChannelIndex: ClientMetadata[int]
    """
    The index of the channel that should be used. This value is 0-indexed, i.e. the first channel has index 0, the second one index 1 and so on.
    """
