import asyncio
import configparser
import datetime

import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as font
from async_tkinter_loop import async_handler, async_mainloop

# import numato_gpio

from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper_asyncio import scancodes, capscodes, evdev_readline


class Application(tk.Frame):
    """
    Define application window and widget parameters,
    widget handlers
    """
    cycle_start_stop = False

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.canvas = tk.Canvas(master=window, width=640, height=200)

        self.btn_cycle_start_stop = tk.Button(self,
                                              text="Tap to enable",
                                              command=async_handler(self.btn_cycle_start_stop_handler),
                                              width=20, height=10,
                                              font=font.Font(size=14),
                                              fg="white", activeforeground="white",
                                              activebackground="darkgreen", bg="darkgreen"
                                              )
        self.btn_cycle_start_stop.pack(side="left", fill=tk.BOTH, expand=tk.YES)

        self.IO_text = tkst.ScrolledText()
        self.IO_text.pack(side="right", fill=tk.BOTH, expand=tk.YES)

        self.pack()

    async def btn_cycle_start_stop_handler(self):
        self.cycle_start_stop = not self.cycle_start_stop
        if self.cycle_start_stop is True:
            self.btn_cycle_start_stop["text"] = "Tap to disable"
            self.btn_cycle_start_stop["activeforeground"] = "black"
            self.btn_cycle_start_stop["fg"] = "black"
            self.btn_cycle_start_stop["activebackground"] = "lightgreen"
            self.btn_cycle_start_stop["bg"] = "lightgreen"
        else:
            self.btn_cycle_start_stop["text"] = "Tap to enable"
            self.btn_cycle_start_stop["activeforeground"] = "white"
            self.btn_cycle_start_stop["fg"] = "white"
            self.btn_cycle_start_stop["activebackground"] = "darkgreen"
            self.btn_cycle_start_stop["bg"] = "darkgreen"

async def read_rfid(device, timeout):
    result = None

    try:
        result = await asyncio.wait_for(evdev_readline(device), int(timeout))
    except asyncio.TimeoutError:
        result = 'timeout'

    return result

async def main_work_loop():
    while True:

        if app.cycle_start_stop:
            # print("Worker invoked - app cycle is started")
            clean_buffer = await read_rfid(rfid_reader, 0.5)
            print("Clean buffer: %s" % clean_buffer)

            current_datetime = datetime.datetime.now()
            current_datetime_formatted = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # app.IO_text.delete (1.0, tk.END)

            conveyor_sensor = 1
            # conveyorSensor = numato_gpio.read(config['GpioDeviceSettings']['PortConveyorSensor'])
            if conveyor_sensor == 1:
                app.IO_text.insert(tk.END, "%s: RFID tag detected\n" % current_datetime_formatted)

                app.IO_text.insert(tk.END, "%s: Read output of RFID reader\n" % current_datetime_formatted)

                app.IO_text.see("end")

                rfid_tag_id = await read_rfid(rfid_reader, rfid_reader_timeout)
                app.IO_text.insert(tk.END, "%s: RFID tag: %s\n" % (current_datetime_formatted, rfid_tag_id))

                app.IO_text.insert(tk.END, "\n")
            else:
                app.IO_text.insert(tk.END, "%s: RFID tag not detected\n" % current_datetime_formatted)

            app.IO_text.see("end")

        await asyncio.sleep(0.1)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # numato_gpio = numato_gpio.numato_gpio(
    #     config['GpioDeviceSettings']['Name'],
    #     config['GpioDeviceSettings']['Speed'],
    #     timeout=1)
    #
    rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    rfid_reader_timeout = int(config['RfidReaderDeviceSettings']['Timeout'])
    rfid_reader.grab()
    #
    # # 1 = unmask, 0 = mask
    # numato_gpio.iomask(int("1111111111111111",2))
    # # 1 = input, 0 = output
    # numato_gpio.iodir(int("1111111111111111",2))
    #
    window = tk.Tk()

    app = Application(master=window)

    window.minsize(width=1000, height=250)

    asyncio.get_event_loop_policy().get_event_loop().create_task(main_work_loop())

    async_mainloop(window)
