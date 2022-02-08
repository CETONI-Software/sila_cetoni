import logging
import os
import platform
import uuid
from configparser import ConfigParser
from typing import Dict, Optional


class Config:
    """
    Helper class to read and write a persistent configuration file
    """

    __config_path: str
    __parser: ConfigParser

    def __init__(self, name: str, subdir: str = "") -> None:
        """
        Construct a `Config` that will read from / write to a config file with the given `name`

            :param name: Name of the config file
            :param subdir: (optional) The sub directory to store the config file in
        """
        self.__config_path = os.path.join(self.__config_dir(subdir), name + ".ini")
        self.__parser = ConfigParser()
        if not self.__parser.read(self.__config_path):
            logging.warning(f"Could not read config file! Creating a new one ({self.__config_path}")
            self.__add_default_values()
            self.write()

    @staticmethod
    def __config_dir(self, subdir: str = "") -> str:
        """
        Returns the path to the directory where the configuration file is located
        """
        if platform.system() == "Windows":
            return os.path.join(os.environ["APPDATA"], "sila_cetoni", subdir)
        else:
            return os.path.join(os.environ["HOME"], ".config", "sila_cetoni", subdir)

    def __add_default_values(self):
        """
        Sets all necessary entries to default values
        """
        self.__parser["server"] = {}
        self.__parser["server"]["uuid"] = str(uuid.uuid4())
        self.__parser["pump"] = {}
        self.__parser["axis_position_counters"] = {}

    def write(self):
        """
        Writes the current configuration to the file
        """
        os.makedirs(os.path.dirname(self.__config_path), exist_ok=True)
        with open(self.__config_path, "w") as config_file:
            self.__parser.write(config_file)

    @property
    def server_uuid(self) -> Optional[str]:
        """
        The UUID of the SiLA Server as read from the config file
        """
        return self.__parser["server"].get("uuid")

    @property
    def pump_drive_position_counter(self) -> Optional[int]:
        """
        Returns the pump drive position counter if this config is for a pump device
        """
        return self.__parser["pump"].getint("drive_position_counter")

    @pump_drive_position_counter.setter
    def pump_drive_position_counter(self, drive_position_counter: int):
        self.__parser["pump"]["drive_position_counter"] = str(drive_position_counter)

    @property
    def axis_position_counters(self) -> Optional[Dict[str, int]]:
        """
        Returns the axis position counters if this config is for an axis device
        The keys of the returned dictionary are the axis names and the values are
        the position counter values.
        """
        return self.__parser["axis_position_counters"]

    @axis_position_counters.setter
    def axis_position_counters(self, position_counters: Dict[str, int]):
        logging.info(position_counters)
        self.__parser["axis_position_counters"] = position_counters
