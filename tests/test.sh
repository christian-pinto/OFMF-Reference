#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "Script dir: $SCRIPT_DIR"


cd ${SCRIPT_DIR}/..


python emulator.py -p 5002 -redfish-path ./Resources/CXLAgent/ > agent_logs 2>&1 &

sleep 10

python -m pytest tests/test.py -vvvv
