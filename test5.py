#!/usr/bin/env python
# encoding: utf-8

import sys
import signal
from select import select

def interrupted(signum, frame):
    print ("interrupted!")


def putch(ch):
    sys.stdout.write(ch)

def getch():
    return sys.stdin.read(1)

def getche():
    ch = getch()
    putch(ch)
    return ch

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr <> []

def kbwait(timeout):
    dr,dw,de = select([sys.stdin], [], [], timeout)
    if dr <> []:
        return raw_input()
    else:
        return ""


def main():
    print("start")


    #signal.signal(signal.SIGALRM, interrupted)
    #signal.alarm(5)

    #c=sys.stdin.read(1)

#    nnn=0;
#    while not kbhit():
#        nnn=nnn+1
#    print(nnn);
#    c=getch()
#    print(c)

    aaa=kbwait(10)
    print(aaa)

    #signal.alarm(0)

    print("end")

if __name__ == '__main__':
    main()
