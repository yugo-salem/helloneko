#!/usr/bin/env python
# encoding: utf-8

import curses
import time
import locale

locale.setlocale(locale.LC_ALL,"")


myscreen=curses.initscr()
myscreen.keypad(True)
curses.halfdelay(10)
curses.noecho()


win=curses.newwin(15, 79, 1, 1)
win.scrollok(True)
win2=curses.newwin(4, 79, 16, 1)
win2.scrollok(True)


postbufstr=""


start_time=time.time()
nnn=0

key=""
while key!="KEY_F(1)":

    try:
        key=myscreen.getkey()
    except curses.error:
        key=""

    elapsed_time=time.time()-start_time

    if elapsed_time>3:
        start_time=time.time()
        win.addstr("nnn=%08X %.3f\n"%(nnn,elapsed_time))
        nnn=nnn+1
        win.refresh()


    if key[0:4]!="KEY_":
        postbufstr=postbufstr+key
    if key=="KEY_BACKSPACE":
        postbufstr=postbufstr[:-1]
    if key=="\n":
        win.addstr(postbufstr)
        postbufstr=""
        win.refresh()
    win2.clear()
    win2.addstr(">"+postbufstr)
    win2.refresh()


curses.endwin()
