import time
from flask import Flask, Response, redirect, request, url_for
from app import app

from monitor import MyStreamMonitor

stream = MyStreamMonitor()

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                yield "data: %s\n\n" % (stream.get_count())
                time.sleep(.5)
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index.html'))