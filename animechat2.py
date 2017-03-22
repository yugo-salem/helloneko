#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=bad-whitespace
# pylint: disable=missing-docstring

from __future__ import unicode_literals
import sys
import os
# import datetime
from datetime import datetime
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


INDEX_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        {messages}
        <form action="/postmsg">
            message:<br>
            <input type="text" name="username" value="">
            <br>
            <textarea rows="5" cols="50" name="msg"></textarea>
            <br>
            <input type="submit" value="Post">
        </form>
    </body>
    </html>
"""

MESSAGE_TEMPLATE = """
    <p>
        <i>{username} {datetime}</i>
        <b>{text}</b>
    </p>
"""


def animechat():
    global messages

    messages_template = ''.join([
        MESSAGE_TEMPLATE.format(datetime=datetime.fromtimestamp(message['ts']),
                                text=message['text'],
                                username=message['user'])
        for message in messages
    ])

    return INDEX_TEMPLATE.format(messages=messages_template)


def htmlpost():
    global msgforpost
    msgforpost=request.args["msg"]
    print(request.args)
    print(msgforpost)
    #return redirect(request.referrer)
    return redirect(url_for("animechat"))
    #return "posted"



def shutdown():
    global exitflag
    exitflag=True
    func=request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'








def main():

    locale.setlocale(locale.LC_ALL,"")

    app=Flask("nekochat")
    app.add_url_rule('/', view_func=hello)
    app.add_url_rule('/animechat', view_func=animechat)
    app.add_url_rule('/postmsg', view_func=htmlpost)
    app.add_url_rule('/shutdown', view_func=shutdown)
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


    global messages
    global msgforpost
    while not exitflag:
        print("update")
        if msgforpost:
            sbot.post(friendchannel,msgforpost)
            msgforpost=None
        messages=sbot.getmsg(friendchannel,30)
        time.sleep(3);

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
