from configparser import ConfigParser
import logging
import os
import platform
from typing import Optional
import uuid


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
            os.makedirs(os.path.dirname(self.__config_path), exist_ok=True)
            with open(self.__config_path, "w") as config_file:
                self.__parser.write(config_file)

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

    @property
    def server_uuid(self) -> Optional[str]:
        """
        The UUID of the SiLA Server as read from the config file
        """
        try:
            return self.__parser["server"]["uuid"]
        except KeyError:
            return None
