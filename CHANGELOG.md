# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of changes

    `Added` for new features.
    `Changed` for changes in existing functionality.
    `Deprecated` for soon-to-be removed features.
    `Removed` for now removed features.
    `Fixed` for any bug fixes.
    `Security` in case of vulnerabilities.
-->

## Unreleased

## v1.8.0

Sync with submodule v1.8.0 releases

### Changed

- Bump required sila2 version to v0.10.1
- Increase required Python version to 3.8 because in 3.7 the implementation of `ThreadPoolExecutor` in the standard library does not reuse idle threads leading to an ever increasing number of threads which eventually causes blocking of the server(s) on Raspberry Pis

## v1.7.1

Sync with submodule v1.7.1 releases

### Fixed

- Typo in pyproject.toml

## v1.7.0

Sync with submodule v1.7.0 releases

### Changed

- Bump required sila2 version to v0.10.0

## v1.6.0

Sync with submodule v1.6.0 releases

## v1.5.0

Sync with submodule v1.5.0 releases

## v1.4.2

sila_cetoni_application v1.4.2 hotfix release

## v1.4.1

sila_cetoni_application v1.4.1 hotfix release

### Fixed

- Add missing dependencies in pyproject.toml

## v1.4.0

Sync with submodule v1.4.0 releases

## v1.3.1

Sync with sila_cetoni_application v1.3.1 hotfix release

## v1.3.0

Sync with submodule v1.3.0 releases

## v1.2.0

### Added

- `DeviceDriverABC` as the abstract base class for all device driver interface classes

## v1.1.0

### Fixed

- Fix dependencies in pyproject.toml

## v1.0.0

First release of sila_cetoni

### Added

- Plugins for
    - the main application
    - CETONI core SiLA 2 Features
    - CETONI controllers SiLA 2 Features
    - CETONI I/O SiLA 2 Features
    - CETONI syringe and contiflow pumps SiLA 2 Features
    - CETONI axis systems SiLA 2 Features
    - CETONI valves SiLA 2 Features
