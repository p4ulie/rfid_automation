#!python3

import asyncio
import configparser
from datetime import datetime, timezone

import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as font
from async_tkinter_loop import async_handler, async_mainloop

import numato_gpio

from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper_asyncio import scancodes, capscodes, evdev_readline

import sqlite3

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
                                              width=10, height=5,
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

def db_log_entry(date, id):
    db_connection.execute('INSERT INTO rfid values (?, ?)', (date, id) )
    db_connection.commit()

async def main_work_loop():

    port_result_ok = config['GpioDeviceSettings']['PortResultOK']
    port_result_nok = config['GpioDeviceSettings']['PortResultNOK']

    while True:
        if app.cycle_start_stop:
            current_datetime = datetime.now()
            current_datetime_formatted = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            # read the value to "clean the buffer"
            clean_buffer = await read_rfid(rfid_reader, 0.5)

            conveyor_sensor_port = config['GpioDeviceSettings']['PortConveyorSensor']
            conveyor_sensor = numato_gpio.read(conveyor_sensor_port)
            # conveyor_sensor = 1

            app.IO_text.insert(tk.END, "%s: Conveyor sensor value: %s\n" % (current_datetime_formatted, conveyor_sensor))

            if conveyor_sensor == 1:
                # app.IO_text.delete (1.0, tk.END)

                numato_gpio.clear(port_result_ok)
                numato_gpio.clear(port_result_nok)

                app.IO_text.insert(tk.END, "%s: RFID tag detected\n" % current_datetime_formatted)
                app.IO_text.insert(tk.END, "%s: Read output of RFID reader\n" % current_datetime_formatted)

                # move the scrolledtext widget position to end
                app.IO_text.see("end")

                # read the RFID tag's ID
                rfid_tag_id = await read_rfid(rfid_reader, rfid_reader_timeout)
                # rfid_tag_id = "999000000020044"

                db_log_entry(datetime.now(timezone.utc), rfid_tag_id)

                if rfid_tag_id != "timeout":
                    app.IO_text.insert(tk.END, "%s: RFID tag: %s, setting port %s\n" % (current_datetime_formatted, rfid_tag_id, port_result_ok))
                    numato_gpio.set(port_result_ok)
                else:
                    app.IO_text.insert(tk.END, "%s: RFID tag not detected, setting port %s\n" % (current_datetime_formatted, port_result_nok))
                    numato_gpio.set(port_result_nok)

            app.IO_text.insert(tk.END, "\n")
            # move the scrolledtext widget position to end
            app.IO_text.see("end")

        await asyncio.sleep(0.1)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    db_file = config['Database_Sqlite']['File']
    print("Open database connection:", db_file)
    db_connection = sqlite3.connect(db_file)
    db_connection.execute("""CREATE TABLE IF NOT EXISTS rfid(
                              date text PRIMARY KEY,
                              id varchar(15) NOT NULL)"""
                          )

    numato_gpio = numato_gpio.numato_gpio(
        config['GpioDeviceSettings']['Name'],
        config['GpioDeviceSettings']['Speed'],
        com_timeout=1
    )

    # initialize the RFID reader and grab the device so system won't catch events
    rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    rfid_reader_timeout = int(config['RfidReaderDeviceSettings']['Timeout'])
    rfid_reader.grab()

    # set port 0 to input, ports 5,6 to output
    numato_gpio.iomask(int("0000000001100001",2))   # 1 = unmask, 0 = mask
    numato_gpio.iodirall(int("0000000000000001",2))   # 1 = input, 0 = output

    window = tk.Tk()
    app = Application(master=window)
    window.minsize(width=1000, height=250)

    # start main work loop
    asyncio.get_event_loop_policy().get_event_loop().create_task(main_work_loop())

    # start GUI event processing loop
    async_mainloop(window)

    db_connection.close()
    print("Database connection closed.")