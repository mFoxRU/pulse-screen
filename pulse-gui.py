__author__ = 'mFoxRU'


import _winreg as reg
import itertools

import Tkinter as tk
import tkMessageBox
import serial
import matplotlib.pyplot as plot
import matplotlib.animation as anim


from stream import Streamer
from fake_stream import FakeStreamer


class PulseGui(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('PulseScreen')
        self.grid()
        self.add_source_interface()
        self.add_control_interface()
        self.add_plot()

    def add_source_interface(self):
        ports = ['Emulate']
        ports.extend([p for p in self._serial_ports()])
        self.port = tk.StringVar()
        self.port.set(ports[0])

        self.source_frame = tk.Frame(self)
        self.source_frame.grid()

        tk.Label(self.source_frame, text='Select input:').grid()
        mn = tk.OptionMenu(
            self.source_frame, self.port, *ports)
        mn.config(width=20)
        mn.grid(column=1, row=0)
        tk.Button(
            self.source_frame, text='Connect', command=self._connect
        ).grid(column=2, row=0)
        tk.Button(
            self.source_frame, text='Quit', command=self._exit
        ).grid(column=3, row=0)

    def add_control_interface(self):
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(column=1, row=0)

        self.channels_num = tk.StringVar()


        isdigcmd = self.register(self._validate_channels)
        tk.Spinbox(self.control_frame, textvariable=self.channels_num,
                   from_=1, to_=100, validate='all',
                   validatecommand=(isdigcmd, '%P')
        ).grid()

        tk.Button(self.control_frame, text=123123123,
                  command=lambda: self.master.title(self.channels_num.get())
        ).grid(column=1, row=0)

        # channels
        # width
        pass

    def add_plot(self):
        pass

    def _validate_channels(self, ch):
        if len(ch):
            return ch.isdigit()
        self.channels_num.set('1')
        return True



    @staticmethod
    def _print(s='qwerty'):
        print s
        return s.isdigit()

    def _connect(self):
        for child in self.source_frame.winfo_children():
            child.configure(state=tk.DISABLED)
        try:
            ser = serial.Serial(self.port.get())
        except serial.SerialException as e:
            tkMessageBox.showerror('Error', e)
            for child in self.source_frame.winfo_children():
                child.configure(state=tk.ACTIVE)
        else:
            ser.close()
            pass

    def _exit(self):
        self.quit()
        self.destroy()

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
