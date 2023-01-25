import datetime, time
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.font as font
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
        self.canvas = tk.Canvas(master=window, width=640, height=200)

        self.btn_cycle_start_stop = tk.Button(self,
                                              text="Tap to enable",
                                              command=self.btn_cycle_start_stop_handler,
                                              width=20, height=10,
                                              font=font.Font(size=14),
                                              fg="white", activeforeground="white",
                                              activebackground="darkgreen", bg="darkgreen"
        )
        self.btn_cycle_start_stop.pack(side="left", fill=tk.BOTH, expand = tk.YES)

        self.IO_text_rfids = tkst.ScrolledText()
        self.IO_text_rfids.pack(side="right", fill=tk.BOTH, expand = tk.YES)

    def btn_cycle_start_stop_handler(self):
        self.cycle_start_stop = not(self.cycle_start_stop)
        if self.cycle_start_stop == True:
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

# def update_rfid_reader():
#     text = ''
#
#     global RFID_tag_ID
#     global thread_run
#
#     while True:
#         evdev_output = evdev_readline(rfid_reader)
#         RFID_tag_ID = "%s:\n%s" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), evdev_output)
#
#         time.sleep(0.5)


def main_work_loop():
    if app.cycle_start_stop:
        current_datetime = datetime.datetime.now()
        current_datetime_formatted = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # app.IO_text_rfids.delete (1.0, tk.END)

        conveyorSensor = 1
        # conveyorSensor = numato_gpio.read(config['GpioDeviceSettings']['PortConveyorSensor'])
        if conveyorSensor == 1:
            app.IO_text_rfids.insert(tk.END, "%s: RFID tag detected\n" % (current_datetime_formatted))
        else
            app.IO_text_rfids.insert(tk.END, "%s: RFID tag not detected\n" % (current_datetime_formatted))

        app.IO_text_rfids.insert(tk.END, "%s: Enable RFID reader\n" % (current_datetime_formatted))
        # numato_gpio.set(config['GpioDeviceSettings']['PortRfidReaderEnable'])
        time.sleep(0.2) # wait for RFID reader to initialize
        app.IO_text_rfids.insert(tk.END, "%s: Read output of RFID reader\n" % (current_datetime_formatted))
        app.IO_text_rfids.insert(tk.END, "%s: Disable RFID reader\n" % (current_datetime_formatted))
        # numato_gpio.clear(config['GpioDeviceSettings']['PortRfidReaderEnable'])

        app.IO_text_rfids.insert(tk.END, "%s: Store time, RFID tag id to DB\n" % (current_datetime_formatted))

        app.IO_text_rfids.insert(tk.END, "%s: Send signal with RFID reading result to result GPIO port (OK/NOK = 1/0)\n" % (current_datetime_formatted))
        # numato_gpio.set(config['GpioDeviceSettings']['PortRfidResult'])
        # numato_gpio.clear(config['GpioDeviceSettings']['PortRfidResult'])

        app.IO_text_rfids.insert(tk.END, "%s: Send signal to indicate the cycle ended to another GPIO port\n" % (current_datetime_formatted))
        # numato_gpio.set(config['GpioDeviceSettings']['PortCycleEnd'])

        app.IO_text_rfids.insert(tk.END, "\n")
        app.IO_text_rfids.see("end")

    window.after(1000, main_work_loop)


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

    window.minsize(width=1000, height=250)
    # window.geometry("250x250")

    window.after(200, main_work_loop)

    # t = threading.Thread(target=update_rfid_reader)
    # t.start()

    app.mainloop()
