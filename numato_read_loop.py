import os
import time
from datetime import datetime
# from distutils.util import strtobool
import numato_gpio

PORT_NAME = os.environ['PORT_NAME']
PORT_SPEED = int(os.environ.get('PORT_SPEED', 19200))

if __name__ == '__main__':
    # Create communication interface
    numato_gpio = numato_gpio.numato_gpio(PORT_NAME, PORT_SPEED, timeout=1)

    # 1 = unmask, 0 = mask
    numato_gpio.iomask(int("1111111111111111",2))
    # 1 = input, 0 = output
    numato_gpio.iodir(int("1111111111111111",2))

    try:
        while True:
            for i in range(5,8):
                print("%s: %d -> %s" % (datetime.now(), i, numato_gpio.read(i)))
            print()
            # print("%s: %s" % (datetime.now(), numato_gpio.readall()))
            # print()
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

    # Close the communication interface
    numato_gpio.close()
