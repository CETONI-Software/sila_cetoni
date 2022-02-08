"""
A device driver implementation for the serial interface of a Sartorius Balance

:author: Florian Meinicke (florian.meinicke@cetoni.de)
:date: 10.01.2022
"""

import logging
import re
import time

import serial
import serial.tools.list_ports

from .balance import BalanceNotFoundException, SerialBalanceInterface


class SartoriusBalanceNotFoundException(BalanceNotFoundException):
    def __init__(self):
        super().__init__(
            "No Sartorius balance detected on any serial port. Please "
            "verify that your balance has the following RS232 settings: "
            "[DAT.REC: SBI], [BAUD: 115200], [PARITY: NONE], [STOPBIT: 1 BIT], "
            "[HANDSHK.: NONE], [DATABITS: 8 BIT]. For best performance, "
            "please ensure that you set COM.SBI -> AUTO.CYCL to EACH VAL."
        )


class SartoriusBalance(SerialBalanceInterface):
    """
    Class for reading serial data from a Sartorius balance
    """

    not_found_exception = SartoriusBalanceNotFoundException

    def __init__(self, port: str = ""):
        super().__init__(port)

    @staticmethod
    def serial_data_to_value(data) -> float:
        # data = 'G     +   0.0006 !  '
        #               ^~~~~~~~~~ match this (and remove spaces later)
        value_regex = re.compile("[+-]?\s+\d+\.\d+")

        return float(value_regex.findall(data)[0].replace(" ", ""))

    def tare(self):
        """
        Executes the tare command
        """
        self._protocol.write_line("T")

    @property
    def unique_balance_identifier_request(self) -> str:
        return "x1_"

    @staticmethod
    def is_valid_balance(data) -> bool:
        # b'Model  BCE124I-1CEU \r\n'
        #                      ^~~~~ positive lookahead   (?=\s+\\r\\n.*)?
        #          ^~~~~~~~~~~~ matches this              [\w\d-]+
        #   ^~~~~~~ positive lookbehind                   (?<=Model\s{2})
        model_regex = re.compile(b"(?<=Model\s{2})[\w\d-]+(?=\s+\\r\\n.*)?")

        return len(model_regex.findall(data)) > 0


# ----------------------------------------------------------------------------
# test
if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(threadName)-12.12s] %(levelname)-8s| %(module)s.%(funcName)s: %(message)s",
        level=logging.DEBUG,
    )

    balance = SartoriusBalance()
    balance.open()
    time.sleep(0.3)
    balance.tare()
    time.sleep(5)
