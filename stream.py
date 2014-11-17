__author__ = 'mFoxRU'

import thread
from itertools import izip

import serial


class LimList(list):
    def __init__(self, iterable, lim=500):
        super(self.__class__, self).__init__(iterable)
        self.lim = lim

    def append(self, p_object):
        super(self.__class__, self).append(p_object)
        while self.__len__() > self.lim:
            self.pop(0)


class Streamer(object):
    _start_bytes = 'ffff'

    def __init__(self, port, speed=9600, channels=3, lim=500):
        try:
            self.port = serial.Serial(port, speed, timeout=0.1)
        except serial.SerialException as e:
            exit(e)
        self._channels = channels
        self._data = LimList([
            [] for _ in xrange(channels)
        ], lim)
        self.locker = thread.allocate_lock()

    @property
    def channels(self):
        return self._channels

    @property
    def data(self):
        with self.locker:
            return self._data

    def calc(self):
        raw = ''
        while 1:
            raw += self.port.readall().encode('hex')
            while len(raw) > 4:
                if raw.startswith(self._start_bytes):
                    info_string = raw[4:4+2*self.channels]
                    print info_string
                    info_bytes = [info_string[x:x+2]
                                  for x in xrange(self.channels)]
                    with self.locker:
                        for data, new in izip(self._data, info_bytes):
                            data.append(int(new, base=16))
                    raw = raw[4+2*self.channels:]
                else:
                    raw = raw[2:]

    def start(self):
        thread.start_new_thread(self.calc, ())