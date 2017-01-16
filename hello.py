#!/usr/bin/env python
# encoding: utf-8


BLINK = '\x1b[5m'
BOLD = '\x1b[1m'
BG_DARK = '\x1b[100m'
WHITE = '\x1b[97m'
MAGENTA = '\x1b[35m'
LIGHT_MAGENTA = '\x1b[105m'
NORMAL = '\x1b[0m\x1b[39m\x1b[49m'
NAME = 'nekochan777'


def main():
    print(''.join([BG_DARK, BOLD, WHITE,
                   'Hello', ' ', BLINK,
                   MAGENTA, NAME, NORMAL]))


    print(''.join([LIGHT_MAGENTA, WHITE, BOLD,
                   ' nekochan + yugo-salem = love <3 ',
                   NORMAL]))

    print(''.join([LIGHT_MAGENTA, WHITE, BOLD,
                   'i wanna be cute nekogirl for my boyfriend yugo-salem !',
                   NORMAL]))

if __name__ == '__main__':
    main()
