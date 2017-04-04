#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=bad-whitespace
# pylint: disable=missing-docstring

import sys
import os
from datetime import datetime
import time
import locale
import threading

import curses
import requests

from flask import Flask, request, redirect, url_for
from flask.templating import render_template_string

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import chatdata

from uimod import uiclass
from slackmod import slackclass


exitflag=False
messages=[]
msgforpost=None


def hello():
    return redirect(url_for("animechat"))






MESSAGES_IFRAME_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        {% for message in messages %}
            <p>
                <i>{{ message["user"] }} {{ message["ts_datetime"] }}</i>
                <br>
                <b>{{ message["text"] }}</b>
            </p>
        {% endfor %}
    </body>
    </html>
"""




def msgs():
    global messages

    if exitflag:
        func=request.environ.get('werkzeug.server.shutdown')
        if func:
            func()

    for message in messages:
        message["ts_datetime"]=datetime.fromtimestamp(message["ts"])

    return render_template_string(MESSAGES_IFRAME_TEMPLATE,messages=messages)



def animechat():
    global messages



ANIMECHAT_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
    </head>
    <body>
        <iframe src="/msgs" width=600 height=300></iframe>
{#
        <form action="{{ url_for('postmsg') }}" method="POST">
#}
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

    tmpstr=""

    tmpstr=tmpstr+"<html>\n"

    tmpstr=tmpstr+"<head>\n"
    tmpstr=tmpstr+"<title>animechat</title>\n"
    tmpstr=tmpstr+'<meta content="text/html;charset=UTF-8">\n'
    tmpstr=tmpstr+"</head>\n"

    tmpstr=tmpstr+"<body>\n"

    tmpstr=tmpstr+'<iframe src="/msgs" width=600 height=300></iframe>\n'

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
    #return redirect(url_for("animechat"))
    #return "posted"
    return redirect("/animechat")








def main():

    locale.setlocale(locale.LC_ALL,"")

    app=Flask("nekochat")
    app.add_url_rule('/', view_func=hello)
    app.add_url_rule('/animechat', view_func=animechat)
    app.add_url_rule('/msgs', view_func=msgs)
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
