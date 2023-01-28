import serial

class numato_gpio(object):
    """Class for sending and receiving data via Numato GPIO board
    Documentation: https://numato.com/docs/16-channel-usb-gpio-module-with-analog-inputs/
    """


    def __init__(self, com_port, com_speed, com_timeout=1, gpio_ports=16):
        """Open serial port at specified baud speed
        Arguments:
            gpio_ports: number of ports on GPIO board
            com_port: serial port number
            com_speed: baud speed
            com_timeout: timeout flag (default enabled)
        """

        self.ports = gpio_ports
        self._MASK_ALL_PORTS = 2 ** self.ports - 1

        self.port = com_port
        self.speed = com_speed
        self.timeout = com_timeout

        #Open port for communication
        self.serPort = serial.Serial(self.port, self.speed, timeout=self.timeout)

    def _getgpioindexstr(self, gpioInput):
        """Convert GPIO input numerical value to hex based character (0-9, A-F)
        string
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        if (int(gpioInput) < 10):
            gpioIndex = str(gpioInput)
        else:
            gpioIndex = str(chr(55 + int(gpioInput)))

        return gpioIndex

    def read(self, gpioInput):
        """Read value on GPIO input
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        payload = "gpio read %s \r" % self._getgpioindexstr(gpioInput)

        self._command(payload)

        response = self.serPort.read_until(b'\r').decode()

        response_value = -1

        if(response[0] == "1"):
            response_value = 1
        elif(response[0] == "0"):
            response_value = 0

        return response_value

    def readadc(self, gpioInput):
        """Read value on ADC input
        Arguments:
            gpioInput: number of the ADC input (0-6)
        """

        payload = "adc read %s \r" % self._getgpioindexstr(gpioInput)

        self._command(payload)

        response = self.serPort.read_until(b'\r').decode()

        response_value = -1

        response_value = int(response)

        return response_value

    def readall(self):
        """Read all value on GPIO inputs in single operation
        Arguments:
        """

        payload = "gpio readall\r"

        self._command(payload)

        response = self.serPort.read_until(b'\r').decode()

        response_value = int(response, 16)

        return response_value

    def writeall(self, gpioInput):
        """Write all values on GPIO in single operation
        Arguments:
            gpioInput: bit encoded set of input to enable (ffff all, 0 none)
        """

        payload = "gpio writeall %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def iodirall(self, gpioInput):
        """Set the direction of all GPIO in single operation
        Arguments:
            gpioInput: bit encoded set of GPIO directions (1 = input, 0 = output)
        """

        payload = "gpio iodir %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def iodir(self, gpioInput, direction):
        """Set the direction of specific GPIO port
        Arguments:
            gpioInput: number of the GPIO input (0-15)
            direction: (1 = input, 0 = output)
        """

       # new_iodir = (self._iodir & ((1 << port) ^ self._MASK_ALL_PORTS)) | (
       #      (0 if not direction else 1) << port
       #  )
       #  self.iodir = new_iodir

        payload = "gpio iodir %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def iomask(self, gpioInput):
        """Set mask for selectively update multiple GPIO with writeall/iodir command
        Arguments:
            gpioInput: bit encoded mask of GPIO directions (1 = unmask, 0 = mask)
        """

        payload = "gpio iomask %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def set(self, gpioInput):
        """Set output status for GPIO input to 1 (high)
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        payload = "gpio set %s\r" % self._getgpioindexstr(gpioInput)

        self._command(payload)

    def clear(self, gpioInput):
        """Set output status for GPIO input to 0 (low)
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        payload = "gpio clear %s\r" % self._getgpioindexstr(gpioInput)

        self._command(payload)

    def _command(self, payload):
        """Run command for GPIO input
        Arguments:
            gpioInput: number of the GPIO input (0-15)
            command: command to write to the GPIO input
        """

        self.serPort.reset_input_buffer()

        self.serPort.write(payload.encode())

        # read echoed command to prepare the buffer
        # for getting the response
        command_echoed = self.serPort.read_until(b'\r')

    def close(self):
        """Close serial port
        Arguments:
        """

        self.serPort.close()