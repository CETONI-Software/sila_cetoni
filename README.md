![SiLA CETONI Logo](doc/sila_header.png)

<!-- omit in toc -->
# sila_cetoni

This repository contains the official [SiLA 2] drivers for a variety of [CETONI devices](https://www.cetoni.com/products/).
These SiLA 2 drivers are based on the [CETONI SDK for Python](https://github.com/CETONI-Software/qmixsdk-for-python) in order to control the devices.

This repository also contains [SiLA 2] drivers for a growing number of third-party devices that can be used in combination with CETONI devices.

- [Getting Started](#getting-started)
  - [Installation](#installation)
    - [sila_cetoni](#sila_cetoni)
    - [CETONI SDK](#cetoni-sdk)
  - [Creating a device configuration](#creating-a-device-configuration)
  - [Running SiLA 2 servers](#running-sila-2-servers)
  - [`sila-cetoni` CLI options reference](#sila-cetoni-cli-options-reference)
- [Troubleshooting](#troubleshooting)
  - ['undefined symbol: __atomic_exchange_8' on Raspberry Pi](#undefined-symbol-__atomic_exchange_8-on-raspberry-pi)
- [Modifying the drivers](#modifying-the-drivers)
- [Contributing](#contributing)

## Getting Started

> **Note**  
> These SiLA 2 drivers were developed and tested under Windows and Linux (Ubuntu 19.04 and Raspbian Buster on a Raspi 3B+) and are therefore expected to work on these systems.
> Other operating system should work as well, but have not been tested yet!

### Installation

#### sila_cetoni

Install the sila_cetoni package with

```console
pip install .
```

It is recommended to install these things in a virtual environment to not interfere with anything in your system's environment.  
This will install all Python dependencies for sila_cetoni most notably `sila_python` as well as sila_cetoni itself.
This means you can not only use the provided console script to run your CETONI device configurations but also build upon the SiLA 2 implementations and build you own applications.

#### CETONI SDK

If you would like to use the CETONI SiLA 2 drivers to control CETONI devices, then you need to install the CETONI SDK with Python Integration.

For instructions on how to install the CETONI SDK for Python on your system and get a valid configuration for your devices see the [CETONI SDK Documentation].  
On Linux be sure to also install the correct SocketCAN driver (either [SysTec](https://www.systec-electronic.com/en/company/support/device-driver/) or [IXXAT](https://www.ixxat.com/support/file-and-documents-download/drivers/socketcan-driver) depending on your CETONI base module).

> **Note**  
> The CETONI SDK is not strictly necessary any more if you only use sila_cetoni to control non-CETONI devices!

### Creating a device configuration

> **Note**  
> If your system contains any CETONI devices you always need a valid CETONI device configuration created with the [CETONI Elements] software in order to use sila_cetoni.  
> If you only want to control a Sartorius balance, for example, you don't need a CETONI device configuration.  
> In any case you need a **sila_cetoni device configuration**.

Starting from version v1.2.0, sila_cetoni uses a device configuration concept similar to the device configurations you can create with the [CETONI Elements] software.  
sila_cetoni's device configuration consists of a single JSON file that describes all the devices you want to have SiLA 2 server for.

The basic structure of this configuration file looks as follows:

```json
{
  "$schema": "https://raw.githubusercontent.com/CETONI-Software/sila_cetoni_application/main/sila_cetoni/application/resources/configuration_schema.json",
  "version": 1,
  "cetoni_devices": {
      "device_config_path": "C:/CETONI_SDK/config/testconfig_qmixsdk"
  }
}
```

This file says that you have no third-party devices and that you want to use the CETONI device configuration located at *C:/CETONI_SDK/config/testconfig_qmixsdk*.

As you can see, you still need the CETONI device configuration created with [CETONI Elements] in order to create SiLA 2 servers for these devices.

Now, if you want to add devices from other vendors that are also supported by sila_cetoni, you need to add these like this:

```json
{
  "$schema": "https://raw.githubusercontent.com/CETONI-Software/sila_cetoni_application/main/sila_cetoni/application/resources/configuration_schema.json",
  "version": 1,
  "cetoni_devices": {
      "device_config_path": "C:/CETONI_SDK/config/testconfig_qmixsdk"
  },
  "devices": {
    "Sartorius Balance": {
      "type": "balance",
      "manufacturer": "Sartorius",
      "port": "COM4"
    }
  }
}
```

Each device is defined in its own object and needs at least the `type` and `manufacturer` properties.
Depending on the device you might also need additional properties, e.g. a serial port as shown here with the balance.  
The name of the property that is used to define a device is used later as the name of the SiLA 2 server that gets created for this device, i.e. the SiLA 2 server created in this example would have th name *Sartorius Balance*.

You can add as many devices as you like in the `devices` object, e.g. if you have two balances you might have the following configuration:

```json
{
  "$schema": "https://raw.githubusercontent.com/CETONI-Software/sila_cetoni_application/main/sila_cetoni/application/resources/configuration_schema.json",
  "version": 1,
  "cetoni_devices": {
      "device_config_path": "C:/CETONI_SDK/config/testconfig_qmixsdk"
  },
  "devices": {
    "Sartorius Balance 1": {
      "type": "balance",
      "manufacturer": "Sartorius",
      "port": "COM4"
    },
    "Sartorius Balance 2": {
      "type": "balance",
      "manufacturer": "Sartorius",
      "port": "COM5"
    }
  }
}
```

> **Note**  
> The `$schema` property is not strictly necessary but VS Code can use that to provide some help when writing the configuration file.
> sila_cetoni will use that schema to validate that the configuration file you provide is correct regardless of whether `$schema` is present or not.

In addition to defining the devices you want to use you can also override most of the command line options that `sila-cetoni` accepts.
That way you can persistently store the options to use with each configuration you create.

The following shows a complete configuration file with all options set to their default values:

```json
{
  "$schema": "https://raw.githubusercontent.com/CETONI-Software/sila_cetoni_application/main/sila_cetoni/application/resources/configuration_schema.json",
  "version": 1,
  "cetoni_devices": {
      "device_config_path": "C:/CETONI_SDK/config/testconfig_qmixsdk"
  },
  "devices": {
    "Sartorius Balance": {
      "type": "balance",
      "manufacturer": "Sartorius",
      "port": "COM4"
    }
  },
  "server_ip": null,
  "server_base_port": 50051,
  "regenerate_certificates": false,
  "log_level": "info",
  "log_file_dir": null,
  "scan_devices": false
}
```

See the [CLI options reference](#sila-cetoni-cli-options-reference) below for mor information about what the individual options do.

### Running SiLA 2 servers

Running the corresponding SiLA 2 servers for your system is always done through the `sila-cetoni` console script that gets installed by `pip`.

Simply run the script giving it the path to the **sila_cetoni device configuration** file as an argument:

```shell
sila-cetoni <path/to/your/device_config.json>
```

By using this device configuration file concept you can easily create multiple device configurations and switch between them by just changing the argument that you call `sila-cetoni` with.

To se a list of all available command line options run

```shell
sila-cetoni --help
```

> **Note**  
> If you have problems running the `sila-cetoni` console script try running the application via the module syntax:
>
> ```shell
> $ python -m sila_cetoni.application <arguments...>
> ```
>
> Also, in case you get the error *ModuleNotFoundError: No module named 'qmixsdk'*
> you have to point the script to the correct location of the CETONI SDK. This can
> easily be done by setting the `CETONI_SDK_PATH` environment variable before calling
> `sila-cetoni`.

You can play around with the servers and their features by using the freely available [SiLA Browser](https://unitelabs.ch/technology/plug-and-play/sila-browser/) or even [CETONI Elements], for example.  
Or you can also write your own SiLA Client software using the Python or any other of the [reference implementations](https://gitlab.com/SiLA2/) of SiLA 2.

### `sila-cetoni` CLI options reference

The following table shows all available CLI options that the `sila-cetoni` console script (or the `sila_cetoni.application.__main__` module) understands:

| CLI option                             | Config file option                       | Default value                | Possible values                                      | Description                                                                                                                                                                                                                                                                                                                                                   |
|----------------------------------------|------------------------------------------|------------------------------|------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-h`, `--help`                         | --                                       | --                           | --                                                   | Description                                                                                                                                                                                                                                                                                                                                                   |
| `-v`, `--version`                      | --                                       | --                           | --                                                   | Description                                                                                                                                                                                                                                                                                                                                                   |
| `-l`, `--log-level` `LEVEL`            | `"log_level": "LEVEL"`                   | "info"                       | "debug", "info", "warning", "critical", "error"      | The log level of the application                                                                                                                                                                                                                                                                                                                              |
| `--log-file-dir` `DIR`                 | `"log_file_dir": "DIR"`                  | *empty*                      | *any file system directory path*                     | The directory to write log files to (if not given log messages will only be printed to standard out)                                                                                                                                                                                                                                                          |
| `-i`, `--server-ip` `IP`               | `"server_ip": "IP"`                      | *the localhost's IP address* | *any valid IP address*                               | The IP address on which the servers should run                                                                                                                                                                                                                                                                                                                |
| `-p`, `--server-base-port` `PORT`      | `"server_base_port": PORT`               | 50051                        | any valid port number (positive integer up to 65535) | The port number for the first SiLA Server                                                                                                                                                                                                                                                                                                                     |
| `--regenerate-certificates`            | `"regenerate_certificates": true\|false` | *not specified*/`false`      | `true`, `false`                                      | Force regeneration of the self-signed certificates (e.g. if the IP address of the machine running the servers changed) - not recommended to be set in the configuration file as this would mean that each time the servers are started they will get a new certificate which could lead to potential problems for clients wanting to connect to these servers |
| `--scan-devices` / `--no-scan-devices` | `"scan_devices": true\|false`            | `--no-scan-devices`/`false`  | `true`, `false`                                      | Automatically scan for supported connected devices (e.g. scan for available Sartorius balances if the sila_cetoni_balance package is installed)                                                                                                                                                                                                               |

## Troubleshooting

### 'undefined symbol: __atomic_exchange_8' on Raspberry Pi

You might get the following error when trying to run the driver on a Raspberry Pi:

```console
Traceback (most recent call last):
  File "/home/pi/sila_cetoni/sila_cetoni.py", line 43, in <module>
    from application.application import Application, DEFAULT_BASE_PORT
  File "/home/pi/sila_cetoni/application/application.py", line 35, in <module>
    from sila2lib.sila_server import SiLA2Server
  File "/home/pi/sila_python/sila_library/sila2lib/sila_server.py", line 36, in <module>
    import grpc
  File "/home/pi/.local/lib/python3.9/site-packages/grpc/__init__.py", line 22, in <module>
    from grpc import _compression
  File "/home/pi/.local/lib/python3.9/site-packages/grpc/_compression.py", line 15, in <module>
    from grpc._cython import cygrpc
ImportError: /home/pi/.local/lib/python3.9/site-packages/grpc/_cython/cygrpc.cpython-39-arm-linux-gnueabihf.so: undefined symbol: __atomic_exchange_8
```

This is a known bug in gRPC (<https://github.com/grpc/grpc/issues/20400>) and there exists a workaround, too (<https://github.com/opencv/opencv/issues/15278#issuecomment-520893950>):  
This workaround is already included in `sila_cetoni/application/__init__.py`:

```py
# ...
env["LD_PRELOAD"] = "/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0"  #< workaround for grpc/grpc#20400
#...
```

## Modifying the drivers

You are, of course, free to play around with the code inside this repository.

The implementation files have been generated using the `sila2-codegen` script that comes with `sila_python`.
Refer to [its documentation](https://gitlab.com/SiLA2/sila_python/-/blob/master/docs/add-and-update-features.md) to see how to add and update existing feature implementations.

This repository uses a separate python package for each Feature Category, e.g. all SiLA Features of the 'de.cetoni/pumps.syringepumps' category are implemented in the `sila_cetoni.pumps.syringepumps` package.

## Contributing

You can change and improve the current implementations, create new Commands, Properties, or even whole new SiLA 2 Features.
If you think your changes might be interesting for us and other users as well, feel free to [open a pull request](https://github.com/CETONI-Software/sila_qmix/compare) on the GitHub project page.
Also, if you have any questions or problems with the drivers, just open an issue and we'll try to help you.

[SiLA 2]: https://sila-standard.com/
[CETONI SDK Documentation]: https://cetoni.de/downloads/manuals/CETONI_SDK/index.html
[CETONI Elements]: https://cetoni.com/cetoni-elements/
