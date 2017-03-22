#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=missing-docstring

from __future__ import unicode_literals, print_function
import sys
import os
from pprint import pprint
from datetime import datetime
import time
import locale
from multiprocessing import Process, Manager

from flask import Flask, request, redirect, url_for
from flask.templating import render_template_string

# from uimod import uiclass
from slackmod import slackclass
import animechat_templates
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    import chatdata
except ImportError:
    print('Create `chatdata.py` and define `token` and `friendname`')
    sys.exit(1)


def create_shared_state():
    manager = Manager()

    namespace = manager.Namespace()
    namespace.messages = []

    post_queue = manager.list()

    return manager, namespace, post_queue


def hello():
    return redirect(url_for("animechat"))


def format_message(shared_state):
    return ''.join([
        render_template_string(animechat_templates.MESSAGE_TEMPLATE,
                               datetime=datetime.fromtimestamp(message['ts']),
                               text=message['text'],
                               username=message['user'])
        for message in shared_state.messages
    ])


def animechat(shared_state):
    def handler():
        messages_template = format_message(shared_state)

        template = {
            False: animechat_templates.NON_AJAX_TEMPLATE,
            True: animechat_templates.AJAX_TEMPLATE,
        }['ajax' in request.args]

        return render_template_string(template, messages=messages_template)

    return handler


def messages(shared_state):
    def handler():
        messages = format_message(shared_state)
        if request.is_xhr:
            return messages

        return render_template_string(
            animechat_templates.MESSAGES_IFRAME_TEMPLATE,
            messages=messages,
        )

    return handler


def htmlpost(shared_state, post_queue):
    def handler():
        if request.method == 'POST':
            message = request.form['msg']
            post_queue.append(message)
        if 'redirect' in request.args:
            return redirect(request.environ['HTTP_REFERER'])
        return render_template_string(animechat_templates.POST_TEMPLATE)

    return handler


def runner(shared_state, post_queue):
    app = Flask("nekochat")

    app.add_url_rule('/',
                     view_func=hello,
                     endpoint='index')
    app.add_url_rule('/animechat',
                     view_func=animechat(shared_state),
                     endpoint='animechat')
    app.add_url_rule('/messages',
                     view_func=messages(shared_state),
                     endpoint='messages')
    app.add_url_rule('/postmsg',
                     view_func=htmlpost(shared_state, post_queue),
                     endpoint='postmsg',
                     methods=('GET', 'POST'))

    app.run()


def main():
    _, shared_state, post_queue = create_shared_state()

    locale.setlocale(locale.LC_ALL, '')

    child = Process(target=runner, args=(shared_state, post_queue, ))
    child.start()

    sbot = slackclass()
    sbot.token = chatdata.token

    sbot.test()

    sbot.get_user_id()
    friendid = sbot.userdict[chatdata.friendname]
    friendchannel = sbot.get_im_id(friendid)

    pprint({
        'username': sbot.username,
        'teamname': sbot.teamname,
        'userid': sbot.user_id,
        'teamid': sbot.team_id,
        'friendid': friendid,
        'friendchannel': friendchannel,
    })
    #sbot.post("@yugosalem","test123")
    sbot.getmsg_print(friendchannel, 3)

    try:
        while True:
            print('update')
            while post_queue:
                sbot.post(friendchannel, post_queue.pop())
            shared_state.messages = sbot.getmsg(friendchannel, 30)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except Exception:
        child.terminate()
        raise

    if child.is_alive():
        child.terminate()

    #time.sleep(1)
    #ui=uiclass()
    #ui.uichannel=friendchannel
    #ui.cursesinit()
    #ui.getmsgfunc=sbot.getmsg
    #ui.postmsgfunc=sbot.post
    #ui.mainloop()
    #ui.cursesdone()

    print('end')


if __name__ == '__main__':
    main()
