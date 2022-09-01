import tkinter as tk

IO_count = range(16)
IO_list = [0 for x in IO_count]
widget_list_oval = []

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

        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")
        #
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=self.master.destroy)
        # self.quit.pack(side="bottom")

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

def update_IO_widgets():
    app.update_IO_widgets()
    window.after(200, update_IO_widgets)  # reschedule event in 2 seconds


if __name__ == '__main__':
    window = tk.Tk()
    app = Application(master=window)
    window.after(200, update_IO_widgets)
    app.mainloop()
