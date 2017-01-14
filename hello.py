#!/usr/bin/env python
# encoding: utf-8


BLINK = '\x1b[5m'
BOLD = '\x1b[1m'
MAGENTA = '\x1b[35m'
NORMAL = '\x1b[0m\x1b[39m'
NAME = 'nekochan777'


def main():
    print(''.join(['Hello', ' ', BLINK, BOLD, MAGENTA, NAME, NORMAL]))


if __name__ == '__main__':
    main()
