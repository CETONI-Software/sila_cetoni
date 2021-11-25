import serial
import serial.threaded
import serial.tools.list_ports
import traceback
import time
import re
import logging


class BalanceNotFoundException(Exception):
    def __init__(self):
        super().__init__("No Sartorius balance detected on any serial port. Please " \
                         "verify that your balance has the following RS232 settings: " \
                         "[DAT.REC: SBI], [BAUD: 115200], [PARITY: NONE], [STOPBIT: 1 BIT], " \
                         "[HANDSHK.: NONE], [DATABITS: 8 BIT]. For best performance, "\
                         "please ensure that you set COM.SBI -> AUTO.CYCL to EACH VAL.")

class ReaderThread(serial.threaded.ReaderThread):
    """
    Implements a serial port read loop and dispatches to a Protocol instance but
    do it with threads.

    Provides the connection from the `SartoriusBalance` instance (which creates
    an instance of this `ReaderThread` class) to the protocol instance
    (`SartoriusBalanceReader`) that is created by this `ReaderThread` so that the
    protocol instance that receives the data from the serial port can set the actual
    value of the balance in the `SartoriusBalance` instance
    """
    balance = None #: SartoriusBalance

    def __init__(self, serial_instance, protocol_factory, balance):
        super().__init__(serial_instance, protocol_factory)
        self.balance: SartoriusBalance = balance

class SartoriusBalanceReader(serial.threaded.LineReader):
    """
    Reads/writes to/from a sartorius balance

    The `SartoriusBalance` instance that is represented is obtained from the
    transport object (a `ReaderThread`) that creates an instance of this reader class
    """

    __balance = None #: SartoriusBalance
    __logger = logging.getLogger('balance_driver')

    # data = 'G     +   0.0006 !  '
    #               ^~~~~~~~~~ match this (and remove spaces later)
    __value_regex = re.compile('[+-]?\s+\d+\.\d+')

    # implements serial.threaded.LineReader ----------------------------------
    def connection_made(self, transport: ReaderThread):
        super().connection_made(transport)
        self.__balance: SartoriusBalance = transport.balance
        self.__logger.debug('port opened')

        # validate that we have a Sartorius Balance
        self.write_line('x1_')
        time.sleep(0.5)
        buffer: bytes = transport.serial.read(transport.serial.in_waiting or 1)#
        while self.TERMINATOR in buffer:
            data, buffer = buffer.split(self.TERMINATOR, 1)
            if data and data.startswith(b'Model'):
                break
        else:
                raise BalanceNotFoundException()

    def handle_line(self, data: str):
        self.__logger.debug('line received: {}'.format(repr(data)))

        try:
            self.__balance.set_value(float(self.__value_regex.findall(data)[0].replace(' ', '')))
        except IndexError:
            pass

    def connection_lost(self, exc):
        if exc:
            traceback.print_exception(exc, exc, None)
        self.__logger.debug('port closed')

class SartoriusBalance():
    """
    Class for reading serial data from a Sartorius balance
    """

    __serial: serial.Serial
    __reader_thread: serial.threaded.ReaderThread
    protocol: SartoriusBalanceReader

    __value: float

    __logger = logging.getLogger('balance_driver')

    def __init__(self, port: str = ""):
        self.__serial = serial.Serial()
        if port:
            self.__serial.port = port
        self.__reader_thread = ReaderThread(self.__serial, SartoriusBalanceReader, self)

    def __autodetect_serial_port(self):
        """
        Goes through all available serial ports of the system and tries to find
        the first port connected to a Sartorius Balance
        """

        # b'Model  BCE124I-1CEU \r\n'
        #                      ^~~~~ positive lookahead   (?=\s+\\r\\n.*)
        #          ^~~~~~~~~~~~ matches this              [\w\d-]+
        #   ^~~~~~~ positive lookbehind                   (?<=Model\s{2})
        model_regex = re.compile(b'(?<=Model\s{2})[\w\d-]+(?=\s+\\r\\n.*)')

        for info in serial.tools.list_ports.comports():
            self.__logger.debug(f"autodetection trying port {info.device}")
            ser = serial.Serial(info.device, timeout=2, write_timeout=2)
            try:
                ser.write(b'x1_\r\n')
                time.sleep(0.1)
                balance_model = model_regex.findall(ser.read(ser.in_waiting or 1))
            except serial.SerialTimeoutException:
                continue

            if balance_model:
                self.__logger.info(f"Sartorius device {balance_model[0]} detected on serial port {ser.port}")
                self.__serial.port = ser.port
                break
        else:
            raise BalanceNotFoundException()

    def open(self, port: str = ""):
        """
        Connects to the balance via the serial port with the given `port`
        """
        if self.__serial.isOpen():
            return

        if not port:
            self.__autodetect_serial_port()
        else:
            self.__serial.port = port

        self.__serial.open()
        if not self.__serial.isOpen():
            raise BalanceNotFoundException()
        self.__reader_thread.start()
        _, self.protocol = self.__reader_thread.connect()

    def close(self):
        """
        Closes the communication to the balance
        """
        self.__reader_thread.close()

    def tare(self):
        """
        Executes the tare command
        """
        self.protocol.write_line('T')

    def value(self) -> float:
        """
        Returns the current value of the balance
        """
        return self.__value

    def set_value(self, value: float):
        """
        Sets the value of the balance to `value`
        """
        self.__value = value


# ----------------------------------------------------------------------------
# test
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s [%(threadName)-12.12s] %(levelname)-8s| %(module)s.%(funcName)s: %(message)s',
        level=logging.DEBUG
    )

    balance = SartoriusBalance()
    balance.open()
    time.sleep(0.3)
    balance.tare()
    time.sleep(5)

