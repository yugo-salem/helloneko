#!/usr/bin/env python
# encoding: utf-8

import sys
import signal
from select import select



def kbwait(timeout):
    dr,dw,de = select([sys.stdin], [], [], timeout)
    if dr <> []:
        return raw_input()
    else:
        return ""


def main():
    print("start")

    while True:
        aaa=kbwait(1)
        print("."),
        print(aaa)


    print("end")

if __name__ == '__main__':
    main()
