#!/usr/bin/env bash
#
# Runs a SiLA 2 server with the demo device configuration
#
#set -x

SILA_VENV_PATH=${0%/*}/.sila_cetoni_venv
source $SILA_VENV_PATH/bin/activate

echo Starting demo server...

export SILA_CETONI_NO_LOG_FILE=1
${0%/*}/sila-cetoni.sh -c ${0%/*}/../config/testconfig_qmixsdk
