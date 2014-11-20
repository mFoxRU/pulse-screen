# from __future__ import division
__author__ = 'mFoxRU'

from itertools import izip

import matplotlib.pyplot as plot
import matplotlib.animation as anim


def animate(i, lines, stream):
    datas = [list(x) for x in stream.data]
    for line, data in izip(lines, datas):
        ndata = []
        if len(data) > 3:
            ndata = [data[0]]
            ndata.extend([
                (data[x]+data[x+1]+data[x+2])/3 for x in xrange(len(data)-2)
            ])
            ndata.append(data[-1])
        else:
            ndata = data

        line.set_data(xrange(len(ndata)), ndata)
    return lines


def style_plot():
    plot.ylabel('Value')
    plot.grid()
    plot.legend(loc='upper right')


def set_fullscreen():
    # http://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
    backend = plot.get_backend()
    win = plot.get_current_fig_manager()
    if backend == 'TkAgg':
        win.resize(*win.window.maxsize())
    else:
        print 'Fullscreen not supported'


def plotter(stream, unite=False, blit=False, fullscreen=False):
    lines = []
    fig = plot.figure()

    if unite:
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
    if fullscreen:
        set_fullscreen()
    animus = anim.FuncAnimation(fig, animate,
                                fargs=(lines, stream), interval=10, blit=blit)
    plot.show()