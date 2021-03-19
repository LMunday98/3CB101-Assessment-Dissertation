import time
from flask import Flask, Response, redirect, request, url_for
from app import app

from monitor import MyStreamMonitor

class MyStreamMonitor(object):
    def __init__(self):
        self.count = 0
    def monitor(self, report_interval=1):
        while True:
            print('class count', self.count)
            self.count += 1 
            time.sleep(.5)
    def get_count(self):
        return self.count

stream = MyStreamMonitor()

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                count = stream.get_count()
                print('web count', count)
                yield "data: %s\n\n" % (count)
                time.sleep(.5)
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index.html'))