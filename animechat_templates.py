# encoding: utf-8

from __future__ import print_function, unicode_literals


AJAX_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
        <!--<meta http-equiv="refresh" content="5">-->
    </head>
    <body>
        <div id="messages">
            {{ messages|safe }}
        </div>

        <form action="{{ url_for('postmsg') }}?redirect" method="POST">
            message:<br>
            <input type="text" name="username" value="">
            <br>
            <textarea rows="5" cols="50" name="msg"></textarea>
            <br>
            <input type="submit" value="Post">
        </form>

        <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
        <script>
            $(function () {
                (function refreshMessages () {
                    $.ajax({
                        url: '{{ url_for('messages') }}',
                        success: function (content) {
                            $('#messages').html(content);
                        }
                    });
                    setTimeout(refreshMessages, 1000);
                })();
            });
        </script>

    </body>
    </html>
"""

NON_AJAX_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
    </head>
    <body>
        <iframe width="100%" height="80%" src="{{ url_for('messages') }}"></iframe>
        <iframe width="100%" height="20%" src="{{ url_for('postmsg') }}?iframe"></iframe>
    </body>
    </html>
"""

POST_TEMPLATE = """
    <html>
    <head>
        <title>animechat</title>
        <meta content="text/html;charset=UTF-8">
    </head>
    <body>
        <form action="{{ url_for('postmsg') }}" method="POST">
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

MESSAGES_IFRAME_TEMPLATE = """
    <html>
    <head>
        <title></title>
        <meta content="text/html;charset=UTF-8">
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        {{ messages|safe }}
    </body>
    </html>
"""

MESSAGE_TEMPLATE = """
    <p>
        <i>{{ username }} {{ datetime }}</i>
        <b>{{ text }}</b>
    </p>
"""
