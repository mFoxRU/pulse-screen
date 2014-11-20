__author__ = 'mFoxRU'

from itertools import izip

import matplotlib.pyplot as plot
import matplotlib.animation as anim


def animate(i, lines, stream):
    datas = [list(x) for x in stream.data]
    for line, data in izip(lines, datas):
        line.set_data(xrange(len(data)), data)
    return lines


def style_plot():
    plot.ylabel('Value')
    plot.grid()
    plot.legend(loc='upper right')


def plotter(stream, split_streams=True):
    lines = []
    fig = plot.figure()

    if not split_streams:
        ax = plot.axes(xlim=(0, stream.lim), ylim=(0, 256))
        for chan in xrange(stream.channels):
            line, = ax.plot([], [], label='Channel {0}'.format(chan+1))
            lines.append(line)
        style_plot()
    else:
        for chan in xrange(stream.channels):
            qax = fig.add_subplot(311+chan, xlim=(0, stream.lim), ylim=(0, 256))
            # x = plot.subplot(210+chan)
            line, = qax.plot([], [], label='Channel {0}'.format(chan+1))
            style_plot()
            lines.append(line)



    plot.xlabel('Time')
    animus = anim.FuncAnimation(fig, animate,
                                fargs=(lines, stream), interval=10, blit=False)
    plot.show()