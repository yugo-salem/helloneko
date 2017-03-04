#!/usr/bin/env python
# encoding: utf-8

import requests
import datetime

def main():

    r=requests.get('https://s2.bitcoinwisdom.com/ticker')

    tmpf=open("aaa","w");
    #tmpf.write(r.text.encode('utf-8'))
#    tmpf.write(r.content)

    rjson=r.json()
#    print(rjson)
    curbtcdatetime=rjson["btcebtcusd"]["date"]
#    print(curbtcdatetime)
    btcusdprice=rjson["btcebtcusd"]["last"]
    print(btcusdprice)

    dt=datetime.datetime.fromtimestamp(curbtcdatetime);
    print(dt)


    r2=requests.get('https://www.bloomberg.com/markets/api/bulk-time-series/price/CO1%3ACOM,USDRUB:CUR')
    tmpf.write(r2.content)
    rjson2=r2.json()
    usdrubprice=rjson2[1]["lastPrice"]
    print(usdrubprice)

    btcrubprice=usdrubprice*btcusdprice
    print("btcrub=%.2f"%btcrubprice)

    tmpf.close()

if __name__ == '__main__':
    main()
