__author__ = 'mFoxRU'

from itertools import izip

import matplotlib.pyplot as plot
import matplotlib.animation as anim


def animate(i, lines, stream):
    datas = [x for x in stream.data]
    for line, data in izip(lines, datas):
        # if data.counter <= data.lim:
        line.set_data(xrange(len(data)), data)
        # else:
        #     line.set_data(range(data.counter-data.lim, data.lim), data)
        #     line
    print 'lines', lines
    return lines


def plotter(stream):
    fig = plot.figure()
    ax = plot.axes(ylim=(0, 256))
    lines = []
    for chan in xrange(stream.channels):
        line, = ax.plot([], [], label='Channel {0}'.format(chan+1))
        lines.append(line)
    plot.xlabel('Time')
    plot.ylabel('Value')
    plot.grid()
    plot.legend(loc='upper right')

    animus = anim.FuncAnimation(fig, animate,
                                fargs=(lines, stream), interval=10, blit=True)
    plot.show()