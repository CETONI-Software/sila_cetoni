@echo off
REM Installs sila_cetoni's dependencies

set SILA_VENV_PATH=%~dp0\.sila_cetoni_venv

echo Installing...

set pip=
for /f %%i in ("pip pip3") do (
    for /f "usebackq tokens=*" %%i in (`where pip3`) do set pip="%%i"
)

if %pip% == "" (
    echo "Could not find a pip executable! Either install pip for python 3 or adjust your PATH environment variable to point to the directory where pip is located."
    exit /b 1
)

set python=
for /f %%i in ("python python3") do (
    for /f "usebackq tokens=*" %%i in (`where python3`) do set python="%%i"
)

if %pip% == "" (
    echo "Could not find a python executable! Either install python 3 or adjust your PATH environment variable to point to the directory where python is located."
    exit /b 1
)

setlocal EnableDelayedExpansion
for /f "usebackq tokens=*" %%i in (`where git`) do set git="%%i"
if %errorlevel% EQU 0 (
    if not %git% == "" (
        %pip% install virtualenv
        %python% -m virtualenv %SILA_VENV_PATH%
        for /f "delims=" %%i in (%pip%) do set pip="%SILA_VENV_PATH%\Scripts\%%~nxi"

        %git% clone -b feature/silacodegenerator-0.3 https://gitlab.com/FMeinicke/sila_python.git %~dp0\sila_python
        for /f %%i in ("sila_library sila_tools/sila2codegenerator") do (
            cd %~dp0\sila_python\%%i
            !pip! install --upgrade .
        )
        cd %~dp0

        !pip! install -r requirements.txt

        echo Done
    )
) else (
    echo "Please install git first and then re-run this script!"
    exit /b 1
)

exit /b
