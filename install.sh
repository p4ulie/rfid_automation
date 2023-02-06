#!/usr/bin/env bash

BASE_NAME="rfid_automation"
INSTALLATION_DIRECTORY="/usr/bin/${BASE_NAME}"

echo "Creating directory ${INSTALLATION_DIRECTORY}..."
mkdir -p "${INSTALLATION_DIRECTORY}"

echo "Copying files..."
cp rfid_automation.py "${INSTALLATION_DIRECTORY}"
cp rfid_automation.sh "${INSTALLATION_DIRECTORY}"
cp rfid_automation.png "${INSTALLATION_DIRECTORY}"
cp rfid_automation.cfg "${INSTALLATION_DIRECTORY}"

cp numato_gpio.py "${INSTALLATION_DIRECTORY}"
cp evdev_text_wrapper_asyncio.py "${INSTALLATION_DIRECTORY}"

#mkdir -p "/etc/${BASE_NAME}"
#cp rfid_automation.cfg "/etc/${BASE_NAME}"

cp rfid_automation.desktop /usr/share/applications/

echo "Setting permissions..."
chmod 755 "${INSTALLATION_DIRECTORY}/rfid_automation.py"
chmod 755 "${INSTALLATION_DIRECTORY}/rfid_automation.sh"
chmod 755 /usr/share/applications/rfid_automation.desktop

echo "Installation finished."

exit 0
