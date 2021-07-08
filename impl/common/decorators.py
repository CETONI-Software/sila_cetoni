"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Decorators*

:details: Decorators:
    Provides some useful decorators for all classes in this module

:file:    decorators.py
:authors: Florian Meinicke
:date (creation)          2021-07-09
:date (last modification) 2021-07-09
________________________________________________________________________
"""

import logging
import functools

from typing import Tuple

# import SiLA errors
from impl.common.qmix_errors import SiLAFrameworkError, SiLAFrameworkErrorType

class InvalidChannelIndex(Exception):
    def __init__(self, invalid_index: int):
        """
        :param invalid_index: The channel index that is invalid
        """
        self.invalid_index = invalid_index

def channel_index(pb2, metadata_key):
    """
    A class decorator that adds helper functions to retrieve the channel index from the
    invocation metadata of a Command call or Property read.
    The decorated class needs to have a public member called `channels` which contains
    a list of all channels that can be used by this class.

    From the functions added by this decorator only one is intended to be used directly: `_get_channel`.
    It receives the `metadata` as first argument and as the second argument a string
    that describes whether the currently handled operation is a Command or Property, e.g.:
        >>> def MyCommand(self, request, context: grpc.ServicerContext):
                channel = self._get_channel(context.invocation_metadata(), "Command")
                # use `channel`...
    This function may also throw an `InvalidChannelIndex` error if the requested
    channel index is not available (i.e. less than 0 or greater than the number of channels)

    :param pb2: The module that contains the `Metadata_ChannelIndex` class
                (e.g. `AnalogInChannelProvider_pb2`)
    :param metadata_key: The key that is used for identifying the metadata value
                         in the invocation metadata list
    """
    def __get_channel_id(self, metadata: Tuple[Tuple[str, str]], type: str) -> str:
        """
        Get the requested channel index from the given `metadata`

        :param metdata: The metadata of the call. It should contain the requested channel index
        :param type: Either "Command" or "Property"
        :return: The channel index if it can be obtained, otherwise a SiLAFrameworkError will be raised
        """

        invocation_metadata = {key: value for key, value in metadata}
        logging.debug(f"Received invocation metadata: {invocation_metadata}")
        try:
            message = pb2.Metadata_ChannelIndex()
            message.ParseFromString(invocation_metadata[metadata_key])
            return message.ChannelIndex.value
        except KeyError:
            raise SiLAFrameworkError(SiLAFrameworkErrorType.INVALID_METADATA,
                                     f'This {type} requires the ChannelIndex metadata!')

    def _get_channel(self, metadata: Tuple[Tuple[str, str]], type: str):
        """
        Get the channel that is identified by the channel name given in `metadata`

        :param metdata: The metadata of the call. It should contain the requested channel name
        :param type: Either "Command" or "Property"
        :return: A valid channel object if the channel can be identified, otherwise a SiLAFrameworkError will be raised
        """

        channel_id = self.__get_channel_id(metadata, type)

        logging.debug(f"Requested channel: {channel_id}")

        if 0 <= channel_id < len(self.channels):
            return self.channels[channel_id]

        raise InvalidChannelIndex(channel_id)

    def decorator_channel_index(cls):
        @functools.wraps(cls)
        def wrapper_channel_index(cls):
            setattr(cls, '__get_channel_id', __get_channel_id)
            setattr(cls, '_get_channel', _get_channel)
            return cls
        return wrapper_channel_index(cls)
    return decorator_channel_index
