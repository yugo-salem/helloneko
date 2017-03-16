#!/usr/bin/env python
# encoding: utf-8

import curses
import time
import locale
import requests
import datetime

import sys, os
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
    uichannel=""

    def cursesinit(self):
        self.myscreen=curses.initscr()
        self.myscreen.keypad(True)
        height,width=self.myscreen.getmaxyx()
        curses.halfdelay(10)
        curses.noecho()
        postwndheight=2
        self.msghistwnd=curses.newwin(height-postwndheight,width-1,0,0)
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
            if not key.startswith("KEY_"):
                postbufstr=postbufstr+key
            self.msgpostwnd.clear()
            self.msgpostwnd.addstr(">"+postbufstr)
            self.msgpostwnd.refresh()

    def test(self):
        payload={"token"  :self.token}
        r=requests.get('https://slack.com/api/auth.test',params=payload)
        #r=requests.get("https://slack.com/api/auth.test?token="+self.token)
        rjson=r.json()
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
        r=requests.get('https://slack.com/api/chat.postMessage',params=payload)
        #print(r.url)
        rjson=r.json()
        #print(rjson)
        resok=rjson["ok"]
        assert resok==True

    def getUserId(self):
        self.userdict=dict()
        self.userreversedict=dict()
        payload={"token"  :self.token}
        r=requests.get('https://slack.com/api/users.list',params=payload)
        rjson=r.json()
        resok=rjson["ok"]
        assert resok==True
        members=rjson["members"]
        nmembers=len(members)
        i=0
        while i<nmembers:
            self.userdict[members[i]["name"]]=members[i]["id"]
            self.userreversedict[members[i]["id"]]=members[i]["name"]
            i=i+1

    def getImId(self,user_id):
        im_id=""
        payload={"token"  :self.token}
        r=requests.get('https://slack.com/api/im.list',params=payload)
        rjson=r.json()
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

    def getmsg(self,channel):
        payload={"token"  :self.token,
                 "channel":channel,
                 "count":"3"}
        r=requests.get('https://slack.com/api/im.history',params=payload)
        rjson=r.json()
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
            dt=datetime.datetime.fromtimestamp(timestamp);
            print(self.userreversedict[msg[i]["user"]]),
            #print(msg[i]["user"]),
            print(dt)
            print(msg[i]["text"])
            i=i+1

    def updatemsglog(self):
        payload={"token"  :self.token,
                 "channel":self.uichannel,
                 "count":"10"}
        r=requests.get('https://slack.com/api/im.history',params=payload)
        rjson=r.json()
        resok=rjson["ok"]
        assert resok==True
        msg=rjson["messages"]
        nmsg=len(msg)
        self.msghistwnd.clear()
        j=0
        while j<nmsg:
            i=nmsg-1-j
            self.msghistwnd.addstr("-----------------\n")
            timestamp=msg[i]["ts"]
            timestamp=int(float(timestamp))
            dt=datetime.datetime.fromtimestamp(timestamp);
            self.msghistwnd.addstr(self.userreversedict[msg[i]["user"]])
            #print(msg[i]["user"]),
            self.msghistwnd.addstr(" ")
            self.msghistwnd.addstr(str(dt))
            self.msghistwnd.addstr("\n")
            msgstr=msg[i]["text"]
            self.msghistwnd.addstr(msgstr.encode('utf-8'))
            self.msghistwnd.addstr("\n")
            j=j+1
        self.msghistwnd.refresh()

    def postmsg(self,msg):
        self.post(self.uichannel,msg.decode('utf-8'))
        self.updatemsglog()



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
    sbot.getUserId()
    friendid=sbot.userdict[chatdata.friendname]
    print("friendid="+friendid)
    friendchannel=sbot.getImId(friendid)
    print("friendchannel="+friendchannel)
    sbot.getmsg(friendchannel)

    time.sleep(1)

    sbot.uichannel=friendchannel
    sbot.cursesinit()
    sbot.mainloop()
    sbot.cursesdone()

    print("end")

if __name__ == '__main__':
    main()
