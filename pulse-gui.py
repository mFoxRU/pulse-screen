__author__ = 'mFoxRU'


import _winreg as reg
import itertools

import Tkinter as tk
import tkMessageBox
import serial
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2TkAgg)

from stream import Streamer
from fake_stream import FakeStreamer

import plotting


# noinspection PyAttributeOutsideInit
class PulseGui(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=200, height=200, padx=5, pady=5)
        self.master.title('PulseScreen')

        # Configure grid
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(1, minsize=100)

        # Add widgets
        self.add_source_interface()
        self.add_interface()
        self.add_plot()

        # Fix for X button exit
        self.master.protocol('WM_DELETE_WINDOW', self._exit)

    def add_source_interface(self):
        ports = ['Emulate']
        ports.extend([p for p in self._serial_ports()])
        self.port = tk.StringVar()
        self.port.set(ports[0])
        self.channels_num = tk.StringVar()

        # Frame
        self.source_frame = tk.LabelFrame(self, text='Input source')
        self.source_frame.grid(column=0, row=0, sticky='w')

        # Source selector
        tk.Label(self.source_frame, text='Port:').grid()
        mn = tk.OptionMenu(self.source_frame, self.port, *ports)
        mn.config(width=15)
        mn.grid(column=1, row=0)

        # Channels selector
        tk.Label(self.source_frame, text='Channels:').grid(column=2, row=0)
        tk.Spinbox(self.source_frame, textvariable=self.channels_num,
                   from_=1, to_=6, state='readonly', width=5
        ).grid(column=3, row=0)

        # Connect button
        tk.Button(
            self.source_frame, text='Connect', command=self._try_to_connect
        ).grid(column=5, row=0, padx=5)

    def add_interface(self):
        # Frame
        self.interface_frame = tk.Frame(self)
        self.interface_frame.grid(column=1, row=0, sticky='e')

        # Exit button
        tk.Button(
            self.interface_frame, text='Quit', command=self._exit
        ).grid(column=0, row=0, padx=5)

    def add_plot(self):
        # Frame
        self.plot_frame = tk.Frame(self)
        self.plot_frame.grid(column=0, row=1, columnspan=2, sticky='nsew')
        # Plot
        self.figure = plotting.Figure()

    def _try_to_connect(self):
        port = self.port.get()
        # Disable interface
        for child in self.source_frame.winfo_children():
            child.configure(state=tk.DISABLED)
        # Using fake source?
        if port == 'Emulate':
            self._start()
            return
        # Check port availability
        try:
            ser = serial.Serial(port)
        except serial.SerialException as e:
            tkMessageBox.showerror('Error', e)
            # Re-enable interface
            for child in self.source_frame.winfo_children():
                if child.__class__ is tk.Spinbox:
                    child.configure(state='readonly')
                else:
                    child.configure(state=tk.ACTIVE)
        else:
            ser.close()
            self._start()

    def _start(self):
        port = self.port.get()
        if port == 'Emulate':
            s = FakeStreamer
        else:
            s = Streamer
        self.stream = s(port, channels=int(self.channels_num.get()), lim=100)
        # Make subplots
        self.lines = plotting.make_split_plots(
            self.figure, self.stream.channels, self.stream.lim)
        # Place on canvas
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(
            side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        # Make animation
        self.animation = plotting.animate(
            self.figure, plotting.ani_fn, self.lines, self.stream, False)
        self.canvas.show()

    def _exit(self):
        self.master.quit()
        self.master.destroy()

    @staticmethod
    def _serial_ports():
        try:
            key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE,
                              r'HARDWARE\DEVICEMAP\SERIALCOMM')
        except WindowsError as e:
            exit(e)
        else:
            for n in itertools.count():
                try:
                    port = reg.EnumValue(key, n)
                    yield str(port[1])
                except EnvironmentError:
                    break



if __name__ == '__main__':
    app = PulseGui()
    app.mainloop()
