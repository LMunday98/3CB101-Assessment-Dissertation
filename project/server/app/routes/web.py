import time
from flask import Flask, Response, redirect, request, url_for, render_template
from app import app

from monitor import MyStreamMonitor

stream = MyStreamMonitor()

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                data = stream.get_boat_data()
                yield "data: %s %s %s %s\n\n" % ("stroke: " + data[0], "seat 2: " + data[1], "seat 3: " + data[2], "bow: " + data[3])
                time.sleep(.1)
        return Response(events(), content_type='text/event-stream')
    # return redirect(url_for('static', filename='index.html'))
    return render_template("index.html")