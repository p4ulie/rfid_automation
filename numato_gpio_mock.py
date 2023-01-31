import serial

class numato_gpio(object):
    """Class for sending and receiving data via Numato GPIO board
    Documentation: https://numato.com/docs/16-channel-usb-gpio-module-with-analog-inputs/
    """

    IN = 1
    OUT = 0

    def __init__(self, com_port, com_speed, com_timeout=1, gpio_ports=16):
        """Open serial port at specified baud speed
        Arguments:
            gpio_ports: number of ports on GPIO board
            com_port: serial port number
            com_speed: baud speed
            com_timeout: timeout flag (default enabled)
        """

        self.com_port = com_port
        self.com_speed = com_speed
        self.com_timeout = com_timeout

        self.gpio_ports = gpio_ports

        #Open port for communication
        # self.serPort = serial.Serial(self.com_port, self.com_speed, timeout=self.com_timeout)

    def _getgpioindexstr(self, gpio_port):
        """Convert GPIO port numerical value to hex based character (0-9, A-F)
        string
        Arguments:
            gpio_port: number of the GPIO port (0-15)
        """

        if (int(gpio_port) < 10):
            gpioIndex = str(gpio_port)
        else:
            gpioIndex = str(chr(55 + int(gpio_port)))

        return gpioIndex

    def read(self, gpio_port):
        """Read value on GPIO port
        Arguments:
            gpio_port: number of the GPIO port (0-15)
        """

        payload = "gpio read %s \r" % self._getgpioindexstr(gpio_port)

        self._command(payload)

        # response = self.serPort.read_until(b'\r').decode()
        #
        # response_value = -1
        #
        # if(response[0] == "1"):
        response_value = 1
        # elif(response[0] == "0"):
        #     response_value = 0

        return response_value

    def readadc(self, gpio_port):
        """Read value on ADC input
        Arguments:
            gpio_port: number of the ADC input (0-6)
        """

        payload = "adc read %s \r" % self._getgpioindexstr(gpio_port)

        self._command(payload)

        # response = self.serPort.read_until(b'\r').decode()

        response_value = 1

        # response_value = int(response)

        return response_value

    def readall(self):
        """Read all value on GPIO ports in single operation
        Arguments:
        """

        payload = "gpio readall\r"

        self._command(payload)

        # response = self.serPort.read_until(b'\r').decode()

        # response_value = int(response, 16)   # return base16 (2 bytes hex) value
        response_value = 1
        return response_value

    def writeall(self, gpio_port):
        """Write all values on GPIO in single operation
        Arguments:
            gpio_port: bit encoded set of input to enable (ffff all, 0 none)
        """

        payload = "gpio writeall %s\r" % str("{0:0{1}x}".format(gpio_port,4))

        self._command(payload)

    def iodirall(self, directions):
        """Set the direction of all GPIO in single operation
        Arguments:
            directions: bit encoded set of GPIO directions (1 = input, 0 = output)
        """

        payload = "gpio iodir %s\r" % str("{0:0{1}x}".format(directions, 4))

        self._command(payload)

    def iomask(self, mask):
        """Set mask for selectively update multiple GPIO with writeall/iodir command
        Arguments:
            mask: bit encoded mask of GPIO directions (1 = unmask, 0 = mask)
        """

        payload = "gpio iomask %s\r" % str("{0:0{1}x}".format(mask, 4))

        self._command(payload)

    def iodir(self, gpio_port, direction):
        """Set the direction of specific GPIO port
        Arguments:
            gpio_port: number of the GPIO port (0-15)
            direction: (1 = input, 0 = output)
        """

        # convert number to binary format string and remove leading "0b" from string
        # bit_iomask = bin(gpio_port).replace("0b", "").zfill(self.gpio_ports)
        bit_iomask = 2 ** gpio_port
        if direction == self.IN:
            bit_iodir = bit_iomask
        else:
            bit_iodir = 0

        self.iomask(bit_iomask)
        self.iodirall(bit_iodir)

    def set(self, gpio_port):
        """Set output status for GPIO port to 1 (high)
        Arguments:
            gpio_port: number of the GPIO port (0-15)
        """

        payload = "gpio set %s\r" % self._getgpioindexstr(gpio_port)

        self._command(payload)

    def clear(self, gpio_port):
        """Set output status for GPIO port to 0 (low)
        Arguments:
            gpio_port: number of the GPIO port (0-15)
        """

        payload = "gpio clear %s\r" % self._getgpioindexstr(gpio_port)

        self._command(payload)

    def _command(self, payload):
        """Run command for GPIO port
        Arguments:
            gpio_port: number of the GPIO port (0-15)
            command: command to write to the GPIO port
        """

        # self.serPort.reset_input_buffer()
        #
        # self.serPort.write(payload.encode())

        # read echoed command to prepare the buffer
        # for getting the response
        # command_echoed = self.serPort.read_until(b'\r')

    def close(self):
        """Close serial port
        Arguments:
        """

        # self.serPort.close()