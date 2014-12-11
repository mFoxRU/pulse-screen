# from __future__ import division
__author__ = 'mFoxRU'

from itertools import izip

from matplotlib.figure import Figure
import matplotlib.animation as anim


def ani_fn(i, lines, stream):
    datas = [list(x[0]) for x in stream.data]
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


def set_fullscreen():
    # http://stackoverflow.com/questions/12439588
    backend = plot.get_backend()
    win = plot.get_current_fig_manager()
    if backend == 'TkAgg':
        win.resize(*win.window.maxsize())
    elif backend == 'wxAgg':
        win.frame.Maximize(True)
    elif backend == 'QT4Agg':
        win.window.showMaximized()
    else:
        print 'Fullscreen not supported'


def style_plot():
    # plot.ylabel('Value')
    # plot.grid()
    # plot.legend(loc='upper right')
    pass


def make_unite_plots(fig, ch, lim):
    lines = []
    ax = fig.axes(xlim=(0, lim), ylim=(0, 256))
    for chan in xrange(ch):
        line, = ax.plot([], [], label='Channel {0}'.format(chan+1))
        lines.append(line)
    style_plot()
    fig
    # plot.xlabel('Time')
    return lines


def make_split_plots(fig, ch, lim):
    lines = []
    if ch <= 3:
        base = 311
    else:
        base = 321
    for chan in xrange(ch):
        qax = fig.add_subplot(base+chan, xlim=(0, lim), ylim=(0, 256))
        # x = plot.subplot(210+chan)
        # qax.xaxis.set_animated(True)
        line, = qax.plot([], [], label='Channel {0}'.format(chan+1))
        style_plot()
        lines.append(line)
    # plot.xlabel('Time')
    return lines


def animate(fig, fn, lines, stream, blit):
    return anim.FuncAnimation(
        fig, fn, fargs=(lines, stream), interval=10, blit=blit)


def plotter(stream, unite=False, blit=False, fullscreen=False):
    fig = Figure()
    lim = stream.lim
    ch = stream.channels
    if unite:
        lines = make_unite_plots(fig, ch, lim)
    else:
        lines = make_split_plots(fig, ch, lim)

    if fullscreen:
        set_fullscreen()
    animation = animate(fig, ani_fn, lines, stream, blit)
    plot.show()


if __name__ == '__main__':
    from fake_stream import FakeStreamer

    astream = FakeStreamer('', 111, 3, 100)

    unite = False

    blit = True

    plotter(astream, unite, blit, False)













