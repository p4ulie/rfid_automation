#!/usr/bin/env bash

INSTALLATION_DIRECTORY="/usr/bin/rfid_automation"

echo "Creating directory ${INSTALLATION_DIRECTORY}..."
mkdir -p "${INSTALLATION_DIRECTORY}"

echo "Copying files..."
cp rfid_automation.py "${INSTALLATION_DIRECTORY}"
cp numato_gpio.py "${INSTALLATION_DIRECTORY}"
cp evdev_text_wrapper_asyncio.py "${INSTALLATION_DIRECTORY}"
cp settings.ini "${INSTALLATION_DIRECTORY}"
cp rfid.png "${INSTALLATION_DIRECTORY}"
cp run.sh "${INSTALLATION_DIRECTORY}"
cp RFID.desktop /usr/share/applications/

