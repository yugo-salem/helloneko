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




class slackbot:
    token=""
    username=""
    teamname=""
    team_id=""
    user_id=""
    userdict=dict()
    userreversedict=dict()
    myscreen=None
    msghistwnd=None
    msgpostwnd=None
    msghistcount=10
    getmsgfunc=None
    postmsgfunc=None
    uichannel=""

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
        #getmsgfunc=self.getmsg
        #messages=self.getmsg(self.uichannel,self.msghistcount//3)
        messages=self.getmsgfunc(self.uichannel,self.msghistcount//3)
        self.msghistwnd.clear()
        nmsg=len(messages)
        i=0
        while i<nmsg:
            msgdatetime=datetime.datetime.fromtimestamp(messages[i]["ts"])
            self.msghistwnd.addstr("-----------------\n")
            self.msghistwnd.addstr(str(messages[i]["user"])+" "+str(msgdatetime)+"\n")
            self.msghistwnd.addstr(messages[i]["text"].encode('utf-8'))
            self.msghistwnd.addstr("\n")
            i=i+1
        self.msghistwnd.refresh()

    def postmsg(self,msg):
        #postmsgfunc=self.post
        #self.post(self.uichannel,msg.decode('utf-8'))
        self.postmsgfunc(self.uichannel,msg.decode('utf-8'))




    def test(self):
        payload={"token"  :self.token}
        reply=requests.get('https://slack.com/api/auth.test',params=payload)
        #reply=requests.get("https://slack.com/api/auth.test?token="+self.token)
        rjson=reply.json()
        #print(rjson)
        resok=rjson["ok"]
        assert resok==True
        self.username=rjson["user"]
        self.teamname=rjson["team"]
        self.team_id=rjson["team_id"]
        self.user_id=rjson["user_id"]

    def post(self,channel,msg):
        payload={"token"  :self.token,
                 "channel":channel,
                 "text"   :msg,
                 "as_user":"1"}
        reply=requests.get('https://slack.com/api/chat.postMessage',params=payload)
        #print(reply.url)
        rjson=reply.json()
        #print(rjson)
        resok=rjson["ok"]
        assert resok==True

    def get_user_id(self):
        self.userdict=dict()
        self.userreversedict=dict()
        payload={"token"  :self.token}
        reply=requests.get('https://slack.com/api/users.list',params=payload)
        rjson=reply.json()
        resok=rjson["ok"]
        assert resok==True
        members=rjson["members"]
        nmembers=len(members)
        i=0
        while i<nmembers:
            self.userdict[members[i]["name"]]=members[i]["id"]
            self.userreversedict[members[i]["id"]]=members[i]["name"]
            i=i+1

    def get_im_id(self,user_id):
        im_id=""
        payload={"token"  :self.token}
        reply=requests.get('https://slack.com/api/im.list',params=payload)
        rjson=reply.json()
        resok=rjson["ok"]
        assert resok==True
        ims=rjson["ims"]
        nims=len(ims)
        i=0
        while i<nims:
            #print(ims[i]["user"])
            if ims[i]["user"]==user_id:
                im_id=ims[i]["id"]
            i=i+1
        return im_id

    def getmsg_print(self,channel):
        payload={"token"  :self.token,
                 "channel":channel,
                 "count":"3"}
        reply=requests.get('https://slack.com/api/im.history',params=payload)
        rjson=reply.json()
        #print(rjson)
        resok=rjson["ok"]
        assert resok==True
        msg=rjson["messages"]
        nmsg=len(msg)
        i=0
        while i<nmsg:
            print("-----------------")
            timestamp=msg[i]["ts"]
            timestamp=int(float(timestamp))
            msgdt=datetime.datetime.fromtimestamp(timestamp)
            print(self.userreversedict[msg[i]["user"]]),
            #print(msg[i]["user"]),
            print(msgdt)
            print(msg[i]["text"])
            i=i+1

    def getmsg(self,channel,n_msg_req):
        payload={"token"  :self.token,
                 "channel":channel,
                 "count":n_msg_req}
        reply=requests.get('https://slack.com/api/im.history',params=payload)
        rjson=reply.json()
        resok=rjson["ok"]
        assert resok==True
        msg=rjson["messages"]
        nmsg=len(msg)
        messages=[]
        j=0
        while j<nmsg:
            i=nmsg-1-j
            timestamp=int(float(msg[i]["ts"]))
            msgdatetime=datetime.datetime.fromtimestamp(timestamp)
            username=self.userreversedict[msg[i]["user"]]
            msgstr=msg[i]["text"]
            messages.append({"ts":timestamp,"user":username,"text":msgstr})
            j=j+1
        return messages




def main():

    locale.setlocale(locale.LC_ALL,"")

    sbot=slackbot()
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
    sbot.getmsg_print(friendchannel)

    time.sleep(1)

    sbot.uichannel=friendchannel
    sbot.cursesinit()
    sbot.getmsgfunc=sbot.getmsg
    sbot.postmsgfunc=sbot.post
    sbot.mainloop()
    sbot.cursesdone()

    print("end")

if __name__ == '__main__':
    main()
