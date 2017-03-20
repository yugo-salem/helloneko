#!/usr/bin/env python
#coding: utf-8

import datetime
import time

import requests



class slackclass:
    token=""
    username=""
    teamname=""
    team_id=""
    user_id=""
    userdict=dict()
    userreversedict=dict()

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
        self.user_id=rjson["user_id"]
        self.team_id=rjson["team_id"]

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

    def getmsg_print(self,channel,qnttmsg):
        payload={"token"  :self.token,
                 "channel":channel,
                 "count":qnttmsg}
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

