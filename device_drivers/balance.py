"""
An interface for implementing a balance device driver for the CETONI SiLA SDK
"""

import time
import re
import logging
import traceback
import serial
import serial.threaded
import serial.tools.list_ports
from typing import Union
from abc import ABC, abstractmethod, abstractstaticmethod


class _ReaderThread(serial.threaded.ReaderThread):
    """
    Implements a serial port read loop and dispatches to a Protocol instance but
    do it with threads.

    Provides the connection from the `SerialBalanceInterface` instance (which creates
    an instance of this `_ReaderThread` class) to the protocol instance
    (`_SerialBalanceReader`) that is created by this `_ReaderThread` so that the
    protocol instance that receives the data from the serial port can set the actual
    value of the balance in the `SerialBalanceInterface` instance
    """
    balance = None #: SerialBalanceInterface

    def __init__(self, serial_instance, protocol_factory, balance):
        super().__init__(serial_instance, protocol_factory)
        self.balance: SerialBalanceInterface = balance

class _SerialBalanceReader(serial.threaded.LineReader):
    """
    Reads/writes to/from a balance via a serial connection

    The `SerialBalanceInterface` instance that is represented is obtained from
    the transport object (a `_ReaderThread`) that creates an instance of this
    reader class
    """

    __balance = None #: SerialBalanceInterface
    __logger = logging.getLogger('balance_driver')

    # implements serial.threaded.LineReader ----------------------------------
    def connection_made(self, transport: _ReaderThread):
        super().connection_made(transport)

        self.__balance: SerialBalanceInterface = transport.balance
        self.__logger.debug('port opened')

        # validate that we have the correct balance
        self.write_line(self.__balance.unique_balance_identifier_request)
        time.sleep(1.5)
        buffer: bytes = transport.serial.read(transport.serial.in_waiting or 1)
        while self.TERMINATOR in buffer:
            data, buffer = buffer.split(self.TERMINATOR, 1)
            if data and self.__balance.is_valid_balance(data):
                break
        else:
                raise self.__balance.not_found_exception()

    def handle_line(self, data: str):
        self.__logger.debug('line received: {}'.format(repr(data)))

        try:
            self.__balance.value = self.__balance.serial_data_to_value(data)
        except IndexError:
            pass

    def connection_lost(self, exc):
        if exc:
            traceback.print_exception(exc, exc, None)
        self.__logger.debug('port closed')

class BalanceInterface(ABC):
    """
    Interface for a balance device driver
    """

    __value: float

    def __init__(self):
        super().__init__()

    @property
    def value(self) -> float:
        """
        Returns the current value of the balance
        """
        return self.__value

    @value.setter
    def value(self, value: float):
        """
        Sets the value of the balance to `value`
        """
        self.__value = value

    @abstractmethod
    def tare(self):
        """
        Tare the balance
        """
        raise NotImplementedError()



class BalanceNotFoundException(Exception):
    """
    An exception that indicates that a balance is not available (any more) over
    a serial connection
    """
    def __init__(self, msg: str = "No balance detected"):
        super().__init__(msg)

class SerialBalanceInterface(BalanceInterface):
    """
    Interface for a balance device driver that uses a serial communication protocol
    """

    # You can derive from `BalanceNotFoundException` to give a more detailed error
    # message. Set `not_found_exception = YourBalanceNotFoundException` in your
    # custom Balance class
    not_found_exception = BalanceNotFoundException

    __serial: serial.Serial
    __reader_thread: serial.threaded.ReaderThread
    _protocol: _SerialBalanceReader

    __logger = logging.getLogger(__name__)

    def __init__(self, port: str = ""):
        """
        :param port: (optional) The serial port of the balance
        """
        super().__init__()

        self.__serial = serial.Serial()
        if port:
            self.__serial.port = port
        self.__reader_thread = _ReaderThread(self.__serial, _SerialBalanceReader, self)

    def _autodetect_serial_port(self):
        """
        Goes through all available serial ports of the system and tries to find
        the first port connected to a Balance
        """

        for info in serial.tools.list_ports.comports():
            self.__logger.debug(f"autodetection trying port {info.device}")
            try:
                ser = serial.Serial(info.device, timeout=2, write_timeout=2)
                # read something from the balance that uniquely identifies it, e.g.
                ser.write(f"{self.unique_balance_identifier_request}\r\n".encode('utf-8'))
                time.sleep(0.1)
                if self.is_valid_balance(ser.read(ser.in_waiting or 1)):
                    self.__logger.info(f"Balance detected on serial port {ser.port}")
                    self.__serial.port = ser.port
                    break
            except (serial.SerialTimeoutException, serial.SerialException):
                continue
        else:
            raise self.not_found_exception()

    def open(self, port: str = ""):
        """
        Connects to the balance via the serial port with the given `port`

        :param port: (optional) The serial port of the balance. If not given,
                     tries to autodetect a balance by trying all available serial
                     ports until a valid port is found
        """
        if self.__serial.isOpen():
            return

        if not port:
            self._autodetect_serial_port()
        else:
            self.__serial.port = port

        self.__serial.open()
        if not self.__serial.isOpen():
            raise self.not_found_exception()
        self.__reader_thread.start()
        _, self._protocol = self.__reader_thread.connect()

    def close(self):
        """
        Closes the communication to the balance
        """
        self.__reader_thread.close()

    @abstractstaticmethod
    def serial_data_to_value(data) -> float:
        """
        Function to convert the `data` read from the balance to a floating point
        value
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def unique_balance_identifier_request(self) -> str:
        """
        This function should return a string containing a request for the balance
        to return some kind of unique identifier or something that can be used to
        identify if the current serial connection uses the correct balance (e.g.
        this could be a request to return the serial number of the balance).
        The response of the device will be passed to the `is_valid_balance()`
        function to validate it.
        """
        raise NotImplementedError()

    @abstractstaticmethod
    def is_valid_balance(data) -> bool:
        """
        This function should return whether `data` indicates that the current
        serial connection is using the correct balance.

        :param data: The serial data which was read as a response to writing the
                     `unique_balance_identifier_request`
        """
        raise NotImplementedError()
