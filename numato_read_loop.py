import os
import time
# from distutils.util import strtobool
import numato_gpio

PORT_NAME = os.environ['PORT_NAME']
PORT_SPEED = int(os.environ.get('PORT_SPEED', 19200))

if __name__ == '__main__':
    # Create communication interface
    numato_gpio = numato_gpio.numato_gpio(PORT_NAME, PORT_SPEED, timeout=1)

    try:
        while True:
            print(numato_gpio.read(1))
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass

    # Close the communication interface
    numato_gpio.close()
