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
        '--channels', action='store', metavar='VALUE', default=3, type=int,
        help='Number of channels in stream')
    parser.add_argument('-f', help='Use fake stream source')

    return parser.parse_args()


def main():
    conf = parse_args()
    if conf.f:
        stream = FakeStreamer(conf.port, channels=conf.channels)
    else:
        stream = Streamer(conf.port, channels=conf.channels)
        stream.start()

    plotter(stream)


if __name__ == '__main__':
    main()