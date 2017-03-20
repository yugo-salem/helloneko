#!/usr/bin/env python
#coding: utf-8

import datetime
import time

import curses



class uiclass:
    myscreen=None
    msghistwnd=None
    msgpostwnd=None
    msghistcount=10
    getmsgfunc=None
    postmsgfunc=None
    uichannel=""
    messages=[]

    def cursesinit(self):
        self.myscreen=curses.initscr()
        self.myscreen.keypad(True)
        height,width=self.myscreen.getmaxyx()
        curses.halfdelay(10)
        curses.noecho()
        postwndheight=2
        self.msghistcount=height-postwndheight
        self.msghistwnd=curses.newwin(self.msghistcount,width-1,0,0)
        self.msghistwnd.scrollok(True)
        self.msgpostwnd=curses.newwin(postwndheight,width-1,height-postwndheight,0)
        self.msgpostwnd.scrollok(True)

    def cursesdone(self):
        curses.endwin()

    def mainloop(self):
        postbufstr=""
        start_time=time.time()
        key=""
        while key!="KEY_F(1)":
            try:
                key=self.myscreen.getkey()
            except curses.error:
                key=""
            elapsed_time=time.time()-start_time
            if elapsed_time>4:
                start_time=time.time()
                self.updatemsglog()
            if key=="KEY_BACKSPACE":
                tmpstr=postbufstr.decode('utf-8')
                tmpstr=tmpstr[:-1]
                postbufstr=tmpstr.encode('utf-8')
                #postbufstr=postbufstr[:-1]
            if key=="\n":
                self.postmsg(postbufstr)
                postbufstr=""
                key=""
                self.updatemsglog()
            if not key.startswith("KEY_"):
                postbufstr=postbufstr+key
            self.msgpostwnd.clear()
            self.msgpostwnd.addstr(">"+postbufstr)
            self.msgpostwnd.refresh()

    def updatemsglog(self):
        self.messages=self.getmsgfunc(self.uichannel,self.msghistcount//3)
        self.msghistwnd.clear()
        nmsg=len(self.messages)
        i=0
        while i<nmsg:
            msgdatetime=datetime.datetime.fromtimestamp(self.messages[i]["ts"])
            self.msghistwnd.addstr("-----------------\n")
            self.msghistwnd.addstr(str(self.messages[i]["user"])+" "+str(msgdatetime)+"\n")
            self.msghistwnd.addstr(self.messages[i]["text"].encode('utf-8'))
            self.msghistwnd.addstr("\n")
            i=i+1
        self.msghistwnd.refresh()

    def postmsg(self,msg):
        self.postmsgfunc(self.uichannel,msg.decode('utf-8'))

