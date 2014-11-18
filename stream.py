__author__ = 'mFoxRU'

import thread
from time import sleep
from itertools import izip

import serial


class LimList(list):
    def __init__(self, iterable, lim=200):
        super(self.__class__, self).__init__(iterable)
        self.lim = lim
        self.counter = len(iterable)

    def append(self, p_object):
        super(self.__class__, self).append(p_object)
        self.counter += 1
        while self.__len__() > self.lim:
            self.pop(0)


class Streamer(object):
    _start_bytes = 'ffff'

    def __init__(self, port, speed=9600, channels=3, lim=200):
        self.serial = serial.Serial(port, speed, timeout=0, rtscts=1)
        self.lim = lim
        self._channels = channels
        self._data = [
            LimList([], lim) for _ in xrange(channels)
        ]
        self.locker = thread.allocate_lock()

    @property
    def channels(self):
        return self._channels

    @property
    def data(self):
        with self.locker:
            return self._data

    def read_port(self, force=True):
        while 1:
            try:
                if not self.serial.isOpen():
                    self.serial.open()
                new_raw = self.serial.readall().encode('hex')
            except Exception as e:
                if force:
                    self.serial.close()
                    sleep(0.1)
                else:
                    self.serial.close()
                    exit(e)
            else:
                return new_raw

    def calc(self):
        raw = ''
        while 1:
            raw += self.read_port()
            while len(raw) >= 10:
                if raw.startswith(self._start_bytes):
                    info_string = raw[4:4+2*self.channels]
                    info_bytes = [info_string[x*2:x*2+2]
                                  for x in xrange(self.channels)]
                    with self.locker:
                        for data, new in izip(self._data, info_bytes):
                            data.append(int(new, base=16))
                    raw = raw[4+2*self.channels:]
                else:
                    raw = raw[2:]

    def start(self):
        thread.start_new_thread(self.calc, ())