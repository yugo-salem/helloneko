#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=bad-whitespace
# pylint: disable=missing-docstring

import sys
import os
import datetime
import time
import locale

import curses
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import chatdata

from uimod import uiclass
from slackmod import slackclass




def main():

    locale.setlocale(locale.LC_ALL,"")

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
    ui.uichannel=friendchannel
    ui.cursesinit()
    ui.getmsgfunc=sbot.getmsg
    ui.postmsgfunc=sbot.post
    ui.mainloop()
    ui.cursesdone()

    print("end")

if __name__ == '__main__':
    main()
