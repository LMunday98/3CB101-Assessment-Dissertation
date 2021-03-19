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
                yield "data: %s %s %s %s\n\n" % (data["stroke"], data["seat2"], data["seat3"], data["seat4"])
                time.sleep(.1)
        return Response(events(), content_type='text/event-stream')
    # return redirect(url_for('static', filename='index.html'))
    return render_template("index.html")