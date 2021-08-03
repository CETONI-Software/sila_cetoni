#!/usr/bin/env bash
#
# Installs sila_cetoni's dependencies
#
#set -x

SILA_VENV_PATH=${0%/*}/.sila_cetoni_venv

echo Installing...

for i in "pip" "pip3"; do
    pip=`which $i`
    [ $? -eq 0 ] && `$pip --version | grep -q 'python 3'`
    [ $? -eq 0 ] && break;
done

[ -z $pip ] && ( echo "Could not find a pip executable! Either install pip for python 3 or adjust your PATH environment variable to point to the directory where pip is located."; exit 1 )

git=`which git`
[ $? -eq 0 -a -n $git ] || ( echo "Please install git first and then re-run this script!"; exit 1 )

$pip install virtualenv
virtualenv $SILA_VENV_PATH
pip=$SILA_VENV_PATH/bin/${pip##*/}

$git clone -b feature/silacodegenerator-0.3 https://gitlab.com/FMeinicke/sila_python.git ${0%/*}/sila_python
for i in "sila_library" "sila_tools/sila2codegenerator"; do
    cd ${0%/*}/sila_python/$i
    $pip install --upgrade .
done
cd ${0%/*}

$pip install -r requirements.txt

echo Done
exit 0
