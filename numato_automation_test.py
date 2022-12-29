import datetime, time
import tkinter as tk
import tkinter.scrolledtext as tkst
import threading
import numato_gpio
import configparser
from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper import scancodes, capscodes, evdev_readline


class Application(tk.Frame):
    cycle_start_stop = False

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        self.canvas = tk.Canvas(master=window, width=320, height=200)

        self.btn_cycle_start_stop = tk.Button(self, text="Enable", command=self.btn_cycle_start_stop_handler, width=20, height=10)
        self.btn_cycle_start_stop.pack(side="bottom")

        self.IO_text_rfids = tkst.ScrolledText()
        self.IO_text_rfids.pack(side="right")

    def btn_cycle_start_stop_handler(self):
        self.cycle_start_stop = not(self.cycle_start_stop)
        if self.cycle_start_stop == True:
            self.btn_cycle_start_stop["text"] = "Disable"
        else:
            self.btn_cycle_start_stop["text"] = "Enable"


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # numato_gpio = numato_gpio.numato_gpio(
    #     config['GpioDeviceSettings']['Name'],
    #     config['GpioDeviceSettings']['Speed'],
    #     timeout=1)
    #
    # rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    # rfid_reader.grab()
    #
    # # 1 = unmask, 0 = mask
    # numato_gpio.iomask(int("1111111111111111",2))
    # # 1 = input, 0 = output
    # numato_gpio.iodir(int("1111111111111111",2))
    #
    window = tk.Tk()
    app = Application(master=window)

    app.mainloop()
