#!/usr/bin/env bash

INSTALLATION_DIRECTORY="/usr/bin/rfid_automation"

cd "${INSTALLATION_DIRECTORY}"

while :
do
  python3 rfid_automation.py
  sleep 1
done