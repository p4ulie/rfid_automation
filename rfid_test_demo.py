import numato_gpio
import configparser
import time
from evdev import InputDevice, categorize, ecodes

def loop():
    while True:
        conveyor_sensor = numato_gpio.read(config['GpioDeviceSettings']['PortConveyorSensor'])
        if conveyor_sensor == 0:
            print("RFID tag detected")
            print("Enable RFID reader")
            time.sleep(0.2) # wait for RFID reader to initialize
            print("Read output of RFID reader")
            print("Disable RFID reader")
            print("Store time, RFID tag id to DB")
            print("Send signal with RFID reading result to result GPIO port (OK/NOK = 1/0)")
            print("Send signal to indicate the cycle ended to another GPIO port")
            print()

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('rfid_test_demo.ini')

    numato_gpio = numato_gpio.numato_gpio(
        config['GpioDeviceSettings']['Name'],
        config['GpioDeviceSettings']['Speed'],
        timeout=1)

    rfid_reader = config['RfidReaderDeviceSettings']['Name']

    loop()

    numato_gpio.close()
