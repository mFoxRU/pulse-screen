__author__ = 'mFoxRU'

from itertools import izip

import matplotlib.pyplot as plot
import matplotlib.animation as anim

from stream import Streamer

port = '\\\\.\\COM3'
channels = 3

## Change me to True in production
FAKE_STREAM = False

###############################################################################
## Fake data stream, coz iDon't have device
from fake_stream import src
fake = [src(255, 600).next for _ in xrange(channels)]
def fake_stream(i, lines, stream):
    for line, data in izip(lines, fake):
        dt = data()
        line.set_data(dt[0], dt[1])
##
###############################################################################


def animate(i, lines, stream):
    datas = [x for x in stream.data]
    for line, data in izip(lines, datas):
        line.set_data(xrange(len(data)), data)
    return lines,


def main():
    stream = Streamer(port, channels=channels)
    stream.start()

    fig = plot.figure()
    ax = plot.axes(xlim=(0, 600), ylim=(0, 256))
    lines = []
    for chan in xrange(channels):
        line, = ax.plot([], [], label='Channel {0}'.format(chan+1))
        lines.append(line)
    plot.xlabel('Time')
    plot.ylabel('Value')
    plot.grid()
    plot.legend(loc='upper right')

    animus = anim.FuncAnimation(fig,
                                fake_stream if FAKE_STREAM else animate,
                                fargs=(lines, stream), interval=17, blit=False)
    plot.show()


if __name__ == '__main__':
    main()