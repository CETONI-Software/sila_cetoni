#!/usr/bin/env bash
#
# Installs sila_cetoni's dependencies
#
#set -x

function fail() {
    echo "ERROR: $@"
    exit 1
}

HERE=`realpath ${0%/*}`
SILA_VENV_PATH=$HERE/.sila_cetoni_venv

echo Installing...

for i in "python" "python3"; do
    python=`which $i`
    [ $? -eq 0 ] && (`$python --version | grep -qi 'python 3'`) > /dev/null 2>&1
    [ $? -eq 0 ] && break;
done

[ -z $python ] && fail "Could not find a python executable! Either install Python 3 or adjust your PATH environment variable to point to the directory where python is located."

for i in "pip" "pip3"; do
    pip=`which $i`
    [ $? -eq 0 ] && (`$pip --version | grep -qi 'python 3'`) > /dev/null 2>&1
    [ $? -eq 0 ] && break;
done

[ -z $pip ] && fail "Could not find a pip executable! Either install pip for Python 3 or adjust your PATH environment variable to point to the directory where pip is located."

git=`which git`
[ $? -eq 0 -a -n $git ] || fail "Please install git first and then re-run this script!"

$pip install virtualenv
$python -m virtualenv $SILA_VENV_PATH
pip=$SILA_VENV_PATH/bin/${pip##*/}

$git clone -b feature/silacodegenerator-0.3 https://gitlab.com/FMeinicke/sila_python.git $HERE/sila_python
for i in "sila_library" "sila_tools/sila2codegenerator"; do
    cd $HERE/sila_python/$i
    $pip install --upgrade .
done
cd $HERE

$pip install -r requirements.txt

echo Done
exit 0
