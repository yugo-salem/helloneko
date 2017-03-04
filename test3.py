#!/usr/bin/env python
# encoding: utf-8

import requests
import datetime

def main():

    r=requests.get('https://s2.bitcoinwisdom.com/ticker')

    tmpf=open("aaa","w");
    #tmpf.write(r.text.encode('utf-8'))
    tmpf.write(r.content)
    print(r.encoding)

    rjson=r.json()
#    print(rjson)
    curbtcdatetime=rjson["btcebtcusd"]["date"]
    print(curbtcdatetime)
    print(rjson["btcebtcusd"]["last"])

    dt=datetime.datetime.fromtimestamp(curbtcdatetime);
    print(dt)

    tmpf.close()

if __name__ == '__main__':
    main()
