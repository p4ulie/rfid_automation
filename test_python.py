import numato_gpio
import configparser
import time

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    numato_gpio = numato_gpio.numato_gpio(
        config['GpioDeviceSettings']['Name'],
        config['GpioDeviceSettings']['Speed'],
        com_timeout=1)

    # # 1 = unmask, 0 = mask
    numato_gpio.iomask(int("1000011000000000",2))
    # # 1 = input, 0 = output
    numato_gpio.iodirall(int("1000000000000000",2))

    # time.sleep(2)
    # print("Clear port %s: %s" % (port, numato_gpio.clear(port)))
    # print("Read port %s: %s" % (port, numato_gpio.read(port)))

    while True:
        port = 5
        print("Clear port %s: %s" % (port, numato_gpio.clear(port)))
        port = 6
        print("Clear port %s: %s" % (port, numato_gpio.clear(port)))

        port = 0
        result_conveyor = numato_gpio.read(port)
        print("Read port %s: %s" % (port, result_conveyor))

        if result_conveyor == 1:

            result_rfid = "1234" # readRFID(timeout=0.2)

            # store in DB

            if result_rfid != "":
                port = 5
                print("Set port %s: %s" % (port, numato_gpio.set(port)))
            else:
                port = 6
                print("Set port %s: %s" % (port, numato_gpio.set(port)))

        time.sleep(1)
