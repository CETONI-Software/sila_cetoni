@echo off
REM Runs a SiLA 2 server with the demo device configuration

REM Bypass "Terminate Batch Job" prompt.
if "%~1" == "-TRAP_CTRL_C" (
    REM Remove the -TRAP_CTRL_C parameter
    shift
) else (
    cd %~dp0
    call < nul %0 -TRAP_CTRL_C %*
    goto :EOF
)

set SILA_VENV_PATH=%~dp0\.sila_cetoni_venv

echo Starting demo server...

set SILA_CETONI_NO_LOG_FILE=1
%SILA_VENV_PATH%\Scripts\python %~dp0\sila_cetoni.py %~dp0\..\..\config\testconfig_qmixsdk
exit /b
