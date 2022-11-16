import time
import tkinter as tk
import tkinter.scrolledtext as tkst
# import asyncio
import threading
# from async_tkinter_loop import async_handler, async_mainloop
import numato_gpio
import configparser
from evdev import InputDevice, categorize, ecodes
from evdev_text_wrapper import scancodes, capscodes

IO_count = range(16)
IO_list = [0 for x in IO_count]
IO_read_enabled = False
RFID_tag_ID = ''
thread_run = True

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.create_IO_labels()
        self.update_IO_widgets()
        self.pack()

    def create_widgets(self):
        self.canvas = tk.Canvas(master=window, width=320, height=200)
        # self.canvas.pack()

        self.btn_IO_read_enable = tk.Button(self, text="Enable", command=self.btn_IO_read_enable)
        self.btn_IO_read_enable.pack(side="bottom")

        self.IO_text_rfids = tkst.ScrolledText()
        # self.IO_text_rfids.pack(side="bottom")
        self.IO_text_rfids.place(x=10, y=115, height=70, width=200)

    def create_IO_labels(self):
        start_x = 10
        start_y = 10
        width = 20
        height = 20
        spacing_x = 10
        spacing_y = 30

        for i in range(8):
            label = tk.Label(text=i)
            label.place(x=start_x + i*(width + spacing_x ) + 2,
                        y=start_y + height + 2)

        for i in range(8):
            label = tk.Label(text=i+8)
            label.place(x=start_x + i*(width + spacing_x ) + 2,
                        y=start_y + height + spacing_y + height + 2)

    def update_IO_widgets(self):
        start_x = 10
        start_y = 10
        width = 20
        height = 20
        spacing_x = 10
        spacing_y = 30

        widget_list_oval = []

        # first row
        for i in range(8):
            if IO_list[i] == 0:
                color = "darkgreen"
            else:
                color = "lightgreen"
            widget_list_oval.append(self.canvas.create_oval(start_x + i*(width + spacing_x),
                                                            start_y,
                                                            start_x + i*(width + spacing_x) + width,
                                                            start_y + height,
                                                            fill=color)
                                    )

        # second row
        for i in range(8):
            if IO_list[i + 8] == 0:
                color = "darkgreen"
            else:
                color = "lightgreen"
            widget_list_oval.append(self.canvas.create_oval(start_x + i*(width + spacing_x),
                                                            start_y + height + spacing_y,
                                                            start_x + i*(width + spacing_x) + width,
                                                            start_y + height + spacing_y + height,
                                                            fill=color)
                                    )

        global RFID_tag_ID

        if RFID_tag_ID != '':
            app.IO_text_rfids.insert(tk.END, RFID_tag_ID+"\n")
            app.IO_text_rfids.see("end")
            RFID_tag_ID = ''

        self.canvas.pack()

    def btn_IO_read_enable(self):
        global IO_read_enabled
        IO_read_enabled = not(IO_read_enabled)
        if IO_read_enabled == True:
            self.btn_IO_read_enable["text"]= "Disable"
        else:
            self.btn_IO_read_enable["text"]= "Enable"

def task_update_IO_widgets():
    if IO_read_enabled == True:
        IO_inputs = numato_gpio.readall()
        IO_inputs_binary_str = "{:016b}".format(IO_inputs)
        # print(IO_inputs_binary_str)
        for i in range(16):
            IO_list[15-i] = int(IO_inputs_binary_str[i])

    app.update_IO_widgets()

    window.after(200, task_update_IO_widgets)  # reschedule event in 2 seconds

def update_rfid_reader():
    event = ''
    caps = False
    text = ''
    key_lookup = None

    global RFID_tag_ID
    global thread_run

    counter = 0

    while thread_run == True:
        counter += 1
    # async for event in rfid_reader.read_loop():
    #     if event.type == ecodes.EV_KEY:
    #         data = categorize(event) # Save the event temporarily to introspect it
    #
    #         # SHIFT pressed?
    #         if (data.scancode == 42) or (data.scancode == 54):
    #             if data.keystate == 1:
    #                 caps = True
    #             if data.keystate == 0:
    #                 caps = False
    #
    #         # decode ASCII from key code
    #         if data.keystate == 1: # Down events only
    #             if caps:
    #                 key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX
    #             else:
    #                 key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX
    #
    #         if (data.scancode != 42) and (data.scancode != 28):
    #             text += key_lookup
    #
    #         # pressed enter/crlf key
    #         if(data.scancode == 28):
    #             # break
    #             #
    #             if text != '':
    #                 RFID_tag_ID = text
    #                 print(text)
    #                 text = ''

        RFID_tag_ID = str(counter)
        time.sleep(0.1)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    numato_gpio = numato_gpio.numato_gpio(
        config['GpioDeviceSettings']['Name'],
        config['GpioDeviceSettings']['Speed'],
        timeout=1)

    # rfid_reader = InputDevice(config['RfidReaderDeviceSettings']['Name'])
    # rfid_reader.grab()

    # 1 = unmask, 0 = mask
    numato_gpio.iomask(int("1111111111111111",2))
    # 1 = input, 0 = output
    numato_gpio.iodir(int("1111111111111111",2))

    window = tk.Tk()
    app = Application(master=window)
    window.after(200, task_update_IO_widgets)

    t = threading.Thread(target=update_rfid_reader)
    t.start()

    app.mainloop()

    thread_run = False

    # rfid_reader.ungrab()
