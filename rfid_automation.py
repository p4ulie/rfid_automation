#!python3

import asyncio
import configparser
from datetime import datetime, timezone
import logging

import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as font
from async_tkinter_loop import async_handler, async_mainloop

import numato_gpio

from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper_asyncio import scancodes, capscodes, evdev_readline

import sqlite3

rfid_tag_id = "empty"
gpio_ports = 16

class Application(tk.Frame):
    """
    Define application window and widget parameters,
    widget handlers
    """
    cycle_start_stop = False
    gpio_states = [0 for x in range(gpio_ports)]

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.frm_buttons = tk.Frame(master=self.master)
        self.frm_buttons.pack(side="left")

        self.btn_cycle_start_stop = tk.Button(
            self.frm_buttons,
            text="Tap\nto\nenable",
            command=async_handler(self.btn_cycle_start_stop_handler),
            width=10, height=5,
            font=font.Font(size=14),
            fg="white", activeforeground="white",
            activebackground="darkgreen", bg="darkgreen"
        )
        self.btn_cycle_start_stop.pack(side="top")

        self.btn_send_OK = tk.Button(
            self.frm_buttons,
            text="Send\nOK\nsignal",
            command=async_handler(btn_send_ok_handler),
            width=10, height=5,
            font=font.Font(size=14)
        )
        self.btn_send_OK.pack(side="top")

        self.btn_send_NOK = tk.Button(
            self.frm_buttons,
            text="Send\nNOK\nsignal",
            command=async_handler(btn_send_nok_handler),
            width=10, height=5,
            font=font.Font(size=14)
        )
        self.btn_send_NOK.pack(side="top")

        self.canvas_ledbar = tk.Canvas(
            master=self.master,
            width=250,
            height=110
        )
        self.canvas_ledbar.pack(side="left")

        self.draw_led_labels()
        self.draw_led_lights(self.gpio_states)

        self.IO_text = tkst.ScrolledText()
        self.IO_text.pack(side="left", fill=tk.BOTH, expand="true")

        self.pack()

    def draw_led_labels(self):
        start_x = 10
        start_y = 10
        width = 20
        height = 20
        spacing_x = 10
        spacing_y = 30

        # first row of labels
        for i in range(8):
            label = tk.Label(master=self.canvas_ledbar, text=i)
            label.place(x=start_x + i*(width + spacing_x ) + 2,
                        y=start_y + height + 2)

        # second row of labels
        for i in range(8):
            label = tk.Label(master=self.canvas_ledbar, text=i+8)
            label.place(x=start_x + i*(width + spacing_x ) + 2,
                        y=start_y + height + spacing_y + height + 2)

    def draw_led_lights(self, gpio_states):
        self.widget_list_oval = []

        start_x = 10
        start_y = 10
        width = 20
        height = 20
        spacing_x = 10
        spacing_y = 30

        # first row of LEDs
        for i in range(8):
            if gpio_states[i] == 0:
                color = "darkgreen"
            else:
                color = "lightgreen"
            self.widget_list_oval.append(
                self.canvas_ledbar.create_oval(
                    start_x + i*(width + spacing_x),
                    start_y,
                    start_x + i*(width + spacing_x) + width,
                    start_y + height,
                    fill=color
                )
            )

        # second row of LEDs
        for i in range(8):
            if gpio_states[i + 8] == 0:
                color = "darkgreen"
            else:
                color = "lightgreen"
            self.widget_list_oval.append(
                self.canvas_ledbar.create_oval(
                    start_x + i*(width + spacing_x),
                    start_y + height + spacing_y,
                    start_x + i*(width + spacing_x) + width,
                    start_y + height + spacing_y + height,
                    fill=color
                )
            )

        self.canvas_ledbar.pack()

    async def btn_cycle_start_stop_handler(self):
        self.cycle_start_stop = not self.cycle_start_stop
        logger.debug("State of the processing set to %s" % self.cycle_start_stop)
        if self.cycle_start_stop is True:
            self.btn_cycle_start_stop["text"] = "Tap\nto\ndisable"
            self.btn_cycle_start_stop["activeforeground"] = "black"
            self.btn_cycle_start_stop["fg"] = "black"
            self.btn_cycle_start_stop["activebackground"] = "lightgreen"
            self.btn_cycle_start_stop["bg"] = "lightgreen"
        else:
            self.btn_cycle_start_stop["text"] = "Tap\nto\nenable"
            self.btn_cycle_start_stop["activeforeground"] = "white"
            self.btn_cycle_start_stop["fg"] = "white"
            self.btn_cycle_start_stop["activebackground"] = "darkgreen"
            self.btn_cycle_start_stop["bg"] = "darkgreen"

async def btn_send_ok_handler():
    logger.debug("Manually triggered send signal OK on port %s" % port_result_ok)
    numato_gpio.set(port_result_ok)

async def btn_send_nok_handler():
    logger.debug("Manually triggered send signal NOK on port %s" % port_result_ok)
    numato_gpio.set(port_result_nok)

def db_log_entry(date, id):
    logger.debug("Storing RFID %s in database with date %s" % (id, date))
    db_connection.execute('INSERT INTO rfid values (?, ?)', (date, id) )
    db_connection.commit()

async def rfid_reader_loop():
    global rfid_tag_id
    while True:
        rfid_tag_id = await evdev_readline(rfid_reader)

async def main_work_loop():
    global rfid_tag_id
    while True:
        gpio_states = [0 for x in range(gpio_ports)]

        gpio_states_bin_str = "{:016b}".format(numato_gpio.readall())
        logger.debug("State of GPIO ports: %s" % gpio_states_bin_str)

        for i in range(gpio_ports):
            gpio_states[15-i] = int(gpio_states_bin_str[i])

        if app is not None:
            app.draw_led_lights(gpio_states)

        logger.debug("Clearing OK/NOK port state")
        numato_gpio.clear(port_result_ok)
        numato_gpio.clear(port_result_nok)

        if app.cycle_start_stop:

            logger.debug("Start new worker cycle")

            # clear the scrolled text widget
            # app.IO_text.delete (0.0, tk.END)

            current_datetime = datetime.now()
            current_datetime_formatted = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            logger.debug("Read conveyor sensor port (%s)" % config['GpioDeviceSettings']['PortConveyorSensor'])
            conveyor_sensor_port = int(config['GpioDeviceSettings']['PortConveyorSensor'])
            # conveyor_sensor = numato_gpio.read(conveyor_sensor_port)
            conveyor_sensor = gpio_states[conveyor_sensor_port]

            # app.IO_text.insert(tk.END, "%s: Conveyor sensor value: %s\n" % (current_datetime_formatted, conveyor_sensor))

            if conveyor_sensor == 1:
                logger.debug("Conveyor sensor triggered")


                app.IO_text.insert(tk.END, "%s: RFID tag detected\n" % current_datetime_formatted)

                # # move the scrolledtext widget position to end
                app.IO_text.see("end")

                logger.debug("Last RFID value detected: %s" % rfid_tag_id)
                if rfid_tag_id != "empty":
                    logger.debug("Send signal OK on port %s" % port_result_ok)
                    app.IO_text.insert(tk.END, "%s: RFID tag: %s, setting port %s\n" % (current_datetime_formatted, rfid_tag_id, port_result_ok))
                    numato_gpio.set(port_result_ok)
                else:
                    logger.debug("Send signal NOK on port %s" % port_result_nok)
                    app.IO_text.insert(tk.END, "%s: RFID tag not detected, setting port %s\n" % (current_datetime_formatted, port_result_nok))
                    numato_gpio.set(port_result_nok)

                db_log_entry(datetime.now(timezone.utc), rfid_tag_id)

                rfid_tag_id = "empty"

            # app.IO_text.insert(tk.END, "\n")
            # move the scrolledtext widget position to end
            app.IO_text.see("end")

        await asyncio.sleep(0.1)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # create logger
    logger = logging.getLogger('rfid_automation')
    logger.setLevel(config['Logging']['Level'])

    # create console handler and set level to debug
    # ch = logging.StreamHandler()
    logger_file = logging.FileHandler(config['Logging']['File'])
    logger_file.setLevel(config['Logging']['Level'])

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    logger_file.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(logger_file)

    # database connection init
    db_file = config['Database_Sqlite']['File']
    logger.debug("Open database %s" % db_file)
    db_connection = sqlite3.connect(db_file)
    logger.debug("Create table if not exists")
    db_connection.execute("""CREATE TABLE IF NOT EXISTS rfid(
                              date text PRIMARY KEY,
                              id varchar(15) NOT NULL)"""
                          )

    logger.debug("Opening GPIO port %s" % config['GpioDeviceSettings']['Name'])
    numato_gpio = numato_gpio.numato_gpio(
        com_port=config['GpioDeviceSettings']['Name'],
        com_speed=config['GpioDeviceSettings']['Speed'],
        com_timeout=1,
        gpio_ports=gpio_ports
    )

    # initialize the RFID reader and grab the device so system won't catch events
    rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    rfid_reader_timeout = int(config['RfidReaderDeviceSettings']['Timeout'])
    rfid_reader.grab()
    logger.debug("RFID reader %s opened" % config['RfidReaderDeviceSettings']['Name'])

    logger.debug("Setting IO mask and direction")
    # set port 0 to input, ports 5,6 to output
    numato_gpio.iomask(int("0000000001100001",2))   # 1 = unmask, 0 = mask
    numato_gpio.iodirall(int("0000000000000001",2))   # 1 = input, 0 = output

    port_result_ok = config['GpioDeviceSettings']['PortResultOK']
    port_result_nok = config['GpioDeviceSettings']['PortResultNOK']

    logger.debug("Creating window")
    window = tk.Tk()
    app = Application(master=window)
    window.minsize(width=1000, height=250)

    logger.debug("Defining asynchronuous RFID reading loop")
    # start RFID reader loop
    asyncio.get_event_loop_policy().get_event_loop().create_task(rfid_reader_loop())

    logger.debug("Defining main worker loop")
    # start main work loop
    asyncio.get_event_loop_policy().get_event_loop().create_task(main_work_loop())

    logger.debug("Starting main window event processing loop")
    # start GUI event processing loop
    async_mainloop(window)

    db_connection.close()
    logger.debug("Database connection closed.")
