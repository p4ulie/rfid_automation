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

    try:
        while True:
            for i in range(16):
                print("%s: %d -> %s" % (datetime.now(), i, numato_gpio.read(i)))
            print()
            print("%s: %s" % (datetime.now(), numato_gpio.readall()))
            print()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    # Close the communication interface
    numato_gpio.close()
