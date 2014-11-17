from __future__ import division
__author__ = 'mFoxRU'

from random import random
from math import sin, cos

from stream import Streamer, LimList


class FakeStreamer(Streamer):
    def __init__(self, port, speed=9600, channels=3, lim=500):
        self._channels = channels
        self._data = LimList([
            [] for _ in xrange(channels)
        ], lim)
        mx = 255
        self.seeds = [random()*random() for _ in xrange(channels)]
        self.fn = lambda x, s: int((mx + mx*sin(x/10)*cos(s*20))/2)
        self._calc = self.calc()


    @property
    def data(self):
        x = self._calc.next()
        return x

    def calc(self):
        step = 0
        while 1:
            for n, data in enumerate(self._data):
                data.append(self.fn(step, self.seeds[n]))
            step += 1
            yield self._data
            
    def start(self):
        pass