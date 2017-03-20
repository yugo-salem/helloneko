#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=bad-whitespace
# pylint: disable=missing-docstring

import sys
import os
import datetime
import time
import locale
import threading

import curses
import requests

from flask import Flask
from flask import request

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import chatdata

from uimod import uiclass
from slackmod import slackclass



globalui=None

app=Flask("nekochat")


def hello():
    curdt=datetime.datetime.now()
    tmpstr=""#"Hello World! "+str(curdt)
    if globalui:
        messages=globalui.messages

    nmsg=len(messages)
    i=0
    while i<nmsg:
        msgdatetime=datetime.datetime.fromtimestamp(messages[i]["ts"])
        tmpstr=tmpstr+"-----------------\n"
        tmpstr=tmpstr+str(messages[i]["user"])+" "+str(msgdatetime)+" \n"
        tmpstr=tmpstr+messages[i]["text"].encode('utf-8')
        tmpstr=tmpstr+"\n"
        i=i+1

    return tmpstr

app.add_url_rule('/', view_func=hello)


def shutdown():
    func=request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

app.add_url_rule('/shutdown', view_func=shutdown)


def worker():
    app.run()



def main():

    locale.setlocale(locale.LC_ALL,"")

    t=threading.Thread(target=worker)
    t.start()
    time.sleep(5)

    sbot=slackclass()
    sbot.token=chatdata.token

    sbot.test()
    print("username="+sbot.username)
    print("teamname="+sbot.teamname)
    print("userid="+sbot.user_id)
    print("teamid="+sbot.team_id)
    #sbot.post("@yugosalem","test123")
    sbot.get_user_id()
    friendid=sbot.userdict[chatdata.friendname]
    print("friendid="+friendid)
    friendchannel=sbot.get_im_id(friendid)
    print("friendchannel="+friendchannel)
    sbot.getmsg_print(friendchannel,3)

    time.sleep(1)

    ui=uiclass()
    global globalui
    globalui=ui
    ui.uichannel=friendchannel
    ui.cursesinit()
    ui.getmsgfunc=sbot.getmsg
    ui.postmsgfunc=sbot.post
    ui.mainloop()
    ui.cursesdone()

    print("end")

if __name__ == '__main__':
    main()
