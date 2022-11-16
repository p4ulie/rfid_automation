import configparser
from evdev import InputDevice, categorize, ecodes
import evdev_text_wrapper

config = configparser.ConfigParser()
config.read('settings.ini')

rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
rfid_reader.grab()

while True:
    rfid = evdev_text_wrapper.readline(rfid_reader)
    if rfid != '':
        print("-", rfid, "-")
