# coding: utf-8


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

ANIMECHAT_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
    </head>
    <body>
        <iframe src="/msgs" width=600 height=300></iframe>
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
