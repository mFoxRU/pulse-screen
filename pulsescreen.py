__author__ = 'mFoxRU'

import argparse

from stream import Streamer
from fake_stream import FakeStreamer
from plotting import plotter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'port', metavar='PORT', help='Appropriate serial port')
    parser.add_argument(
        '-c', dest='channels', action='store', metavar='CHANNELS', default=3,
        type=int, help='Number of channels in stream. Default value is 3')
    parser.add_argument(
        '-f', help='Use fake stream source', action='store_true')
    parser.add_argument(
        '-w', dest='width', metavar='VALUE', type=int, default=600,
        help='Show last VALUE measurement. Default value is 600')
    parser.add_argument(
        '-u', dest='unite', action='store_true',
        help='Show all channels on one plot')
    return parser.parse_args()


def main():
    conf = parse_args()
    if conf.f:
        stream = FakeStreamer(conf.port, channels=conf.channels, lim=conf.width)
    else:
        stream = Streamer(conf.port, channels=conf.channels, lim=conf.width)
        stream.start()

    plotter(stream, conf.unite)


if __name__ == '__main__':
    main()