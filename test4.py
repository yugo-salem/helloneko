#!/usr/bin/env python
# encoding: utf-8

import requests
import datetime


class slackbot:
    token="xoxp-....."
    username=""
    teamname=""
    team_id=""
    user_id=""
    userdict=dict()
    userreversedict=dict()

    def test(self):
        r=requests.get("https://slack.com/api/auth.test?token="+self.token)
        rjson=r.json()
        #print(rjson)
        resok=rjson["ok"]
        assert resok==True
        self.username=rjson["user"]
        self.teamname=rjson["team"]
        self.team_id=rjson["team_id"]
        self.user_id=rjson["user_id"]

    def printinfo(self):
        print(self.username)
        print(self.teamname)
        print(self.user_id)
        print(self.team_id)

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
                 "count":"10"}
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


def main():

    sbot=slackbot()
    sbot.test()
    #sbot.printinfo()
    #sbot.post("@yugosalem","ttttest1")
    sbot.getUserId()
    userid=sbot.userdict["yugosalem"]
    print("userid="+userid)
    imchannel=sbot.getImId(userid)
    print("channel="+imchannel)
    sbot.getmsg(imchannel)

    print("end")

if __name__ == '__main__':
    main()
