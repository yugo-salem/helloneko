#!/usr/bin/env python
# encoding: utf-8

import datetime
import time

from flask import Flask
from flask import request

app = Flask(__name__)


def hello():
    curdt=datetime.datetime.now()
    tmpstr="Hello World! "+str(curdt)
    return tmpstr

app.add_url_rule('/', view_func=hello)


def hello2():
    tmpstr="nyaaa!  :3 "+request.method+" "+request.headers["User-Agent"]
    print(request.args)
    print(request.headers)
    return tmpstr

app.add_url_rule('/bbb', view_func=hello2)


if __name__ == "__main__":
    app.run()
