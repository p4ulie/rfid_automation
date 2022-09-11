import serial

class numato_gpio(object):
    """Class for sending and receiving data via Numato GPIO board
        Documentation: https://numato.com/docs/16-channel-usb-gpio-module-with-analog-inputs/
    """

    def __init__(self, port, speed, timeout=1):
        """Open serial port at specified baud speed
        Arguments:
            port: serial port
            speed: baud speed
            timeout: timeout flag (default enabled)
        """

        self.port = port
        self.speed = speed
        self.timeout = timeout

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

        response = self.serPort.read_until(b'\r')

        response_value = -1

        if(chr(response[-3]) == "1"):
            response_value = 1
        elif(chr(response[-3]) == "0"):
            response_value = 0

        return response_value

    def readall(self):
        """Read all value on GPIO inputs in single operation
        Arguments:
        """

        payload = "gpio readall\r"

        self._command(payload)

        response = self.serPort.read_until(b'\r')

        response_value = response[-3]

        return response_value

    def writeall(self, gpioInput):
        """Write all values on GPIO in single operation
        Arguments:
            gpioInput: bit encoded set of input to enable (ffff all, 0 none)
        """

        payload = "gpio writeall %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def iodir(self, gpioInput):
        """Set the direction of all GPIO in single operation
        Arguments:
            gpioInput: bit encoded set of GPIO directions (1 input, 0 output)
        """

        payload = "gpio iodir %s\r" % str("{0:0{1}x}".format(gpioInput,4))

        self._command(payload)

    def iomask(self, gpioInput):
        """Set mask for selectively update multiple GPIO with writeall/iodir command
        Arguments:
            gpioInput: bit encoded mask of GPIO directions (1 unmask, 0 mask)
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