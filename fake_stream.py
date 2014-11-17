from __future__ import division
__author__ = 'mFoxRU'

from random import random
from math import sin, cos

from stream import LimList


def src(mx=256, lim=300):
    seed = random()*random()
    fn = lambda x: int((mx + mx*sin(x/10)*cos(seed*20))/2)
    data = LimList([], lim)
    step = 0
    while 1:
        data.append(fn(step))
        yield (range(len(data)), data)
        step += 1