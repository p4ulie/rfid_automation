import tkinter as tk
import numato_gpio

PORT_NAME = "/dev/ttyACM1"
PORT_SPEED = 19200

IO_count = range(16)
IO_list = [0 for x in IO_count]
IO_read_enabled = False

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

        self.IO_read_enable = tk.Button(self, text="Enable", command=self.IO_read_enable)
        self.IO_read_enable.pack(side="bottom")

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

        self.canvas.pack()

    def IO_read_enable(self):
        global IO_read_enabled
        IO_read_enabled = not(IO_read_enabled)
        if IO_read_enabled == True:
            self.IO_read_enable["text"]="Disable"
        else:
            self.IO_read_enable["text"]="Enable"

def task_update_IO_widgets():
    if IO_read_enabled == True:
        IO_inputs = numato_gpio.readall()
        IO_inputs_binary_str = "{:016b}".format(IO_inputs)
        # print(IO_inputs_binary_str)
        for i in range(16):
            IO_list[15-i] = int(IO_inputs_binary_str[i])
        app.update_IO_widgets()
    window.after(200, task_update_IO_widgets)  # reschedule event in 2 seconds


if __name__ == '__main__':
    numato_gpio = numato_gpio.numato_gpio(PORT_NAME, PORT_SPEED, timeout=1)

    # 1 = unmask, 0 = mask
    numato_gpio.iomask(int("1111111111111111",2))
    # 1 = input, 0 = output
    numato_gpio.iodir(int("1111111111111111",2))

    window = tk.Tk()
    app = Application(master=window)
    window.after(200, task_update_IO_widgets)
    app.mainloop()
