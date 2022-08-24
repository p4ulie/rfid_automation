# import sys
import serial

class numato_gpio(object):
    """Class for sending and receiving data via Numato GPIO board"""

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

    def read(self, gpioInput):
        """Read value on GPIO input
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        if (int(gpioInput) < 10):
            gpioIndex = str(gpioInput)
        else:
            gpioIndex = chr(55 + int(gpioInput))

        #Send "gpio read" command
        self.serPort.write("gpio read "+ str(gpioIndex) + "\r")

        # Read up to 25 bytes
        response = self.serPort.read(25)

        response_value = -1

        if(response[-4] == "1"):
            response_value = 1

        elif(response[-4] == "0"):
            response_value = 0

        return response_value

    def set(self, gpioInput):
        """Set output status for GPIO input to 1 (high)
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        self.command(gpioInput, "set")

    def clear(self, gpioInput):
        """Set output status for GPIO input to 0 (low)
        Arguments:
            gpioInput: number of the GPIO input (0-15)
        """

        self.command(gpioInput, "clear")

    def command(self, gpioInput, command):
        """Run command for GPIO input
        Arguments:
            gpioInput: number of the GPIO input (0-15)
            command: command to write to the GPIO input
        """

        if (int(gpioInput) < 10):
            gpioIndex = str(gpioInput)
        else:
            gpioIndex = chr(55 + int(gpioInput))

        #Send "gpio read" command
        self.serPort.write("gpio "+ command +" "+ gpioIndex  + "\r")

    def close(self):
        """Close serial port
        Arguments:
        """

        self.serPort.close()