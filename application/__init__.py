import os
import platform

# Change this to point to your CETONI SDK installation path
if platform.system() == "Windows":
    CETONI_SDK_PATH = os.path.join("C:\\", "CETONI_SDK")
    print(f"Running on Windows - setting SDK path to {CETONI_SDK_PATH}")
else:
    try:
        import RPi.GPIO as gpio
        CETONI_SDK_PATH = os.path.join(os.path.expanduser('~'), "CETONI_SDK_Raspi")
        print(f"Running on RaspberryPi - setting SDK path to {CETONI_SDK_PATH}")
    except (ModuleNotFoundError, ImportError):
        CETONI_SDK_PATH = os.path.join(os.path.expanduser('~'), "CETONI_SDK")
        print(f"Running on generic Linux - setting SDK path to {CETONI_SDK_PATH}")
