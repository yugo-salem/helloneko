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

from flask import Flask, request, redirect, url_for

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import chatdata

from uimod import uiclass
from slackmod import slackclass


exitflag=False
messages=[]
msgforpost=None


def hello():
    return redirect(url_for("animechat"))


def animechat():
    global messages

    if exitflag:
        func=request.environ.get('werkzeug.server.shutdown')
        if func:
            func()

    curdt=datetime.datetime.now()
    tmpstr=""

    tmpstr=tmpstr+"<html>\n"

    tmpstr=tmpstr+"<head>\n"
    tmpstr=tmpstr+"<title>animechat</title>\n"
    tmpstr=tmpstr+'<meta content="text/html;charset=UTF-8">\n'
    tmpstr=tmpstr+'<meta http-equiv="refresh" content="5">\n'
    tmpstr=tmpstr+"</head>\n"

    tmpstr=tmpstr+"<body>\n"
    nmsg=len(messages)
    i=0
    while i<nmsg:
        msgdatetime=datetime.datetime.fromtimestamp(messages[i]["ts"])
        tmpstr=tmpstr+"<p>\n"
        tmpstr=tmpstr+"<i>"+str(messages[i]["user"])+" "+str(msgdatetime)+"</i><br>\n"
        tmpstr=tmpstr+"<b>\n"
        tmpstr=tmpstr+messages[i]["text"].encode('utf-8')
        tmpstr=tmpstr+"</b><br>\n"
        tmpstr=tmpstr+"</p>\n"
        i=i+1

    tmpstr=tmpstr+'<form action="/postmsg">\n'
    tmpstr=tmpstr+'message:<br>\n'
    tmpstr=tmpstr+'<input type="text" name="username" value="">\n'
    tmpstr=tmpstr+'<br>\n'
    tmpstr=tmpstr+'<textarea rows="5" cols="50" name="msg"></textarea>\n'
    tmpstr=tmpstr+'<br>\n'
    tmpstr=tmpstr+'<input type="submit" value="Post">\n'
    tmpstr=tmpstr+'</form>\n'

    tmpstr=tmpstr+"</body>\n"
    tmpstr=tmpstr+"</html>\n"

    return tmpstr


def htmlpost():
    global msgforpost
    msgforpost=request.args["msg"]
    print(request.args)
    print(msgforpost)
    #return redirect(request.referrer)
    return redirect(url_for("animechat"))
    #return "posted"








def main():

    locale.setlocale(locale.LC_ALL,"")

    app=Flask("nekochat")
    app.add_url_rule('/', view_func=hello)
    app.add_url_rule('/animechat', view_func=animechat)
    app.add_url_rule('/postmsg', view_func=htmlpost)
    t=threading.Thread(target=app.run)
    t.start()

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


    global exitflag
    global messages
    global msgforpost
    try:
        while not exitflag:
            print("update")
            if msgforpost:
                sbot.post(friendchannel,msgforpost)
                msgforpost=None
            messages=sbot.getmsg(friendchannel,30)
            time.sleep(3);
    except KeyboardInterrupt:
        exitflag=True




    #time.sleep(1)
    #ui=uiclass()
    #ui.uichannel=friendchannel
    #ui.cursesinit()
    #ui.getmsgfunc=sbot.getmsg
    #ui.postmsgfunc=sbot.post
    #ui.mainloop()
    #ui.cursesdone()

    print("end")

if __name__ == '__main__':
    main()
