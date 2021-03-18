#!/usr/bin/env python
from __future__ import division
import itertools
import time
from flask import Flask, Response, redirect, request, url_for
from random import gauss
import threading

app = Flask(__name__)

# Generate streaming data and calculate statistics from it
class MyStreamMonitor(object):
    def __init__(self):
        self.sum   = 0
        self.count = 0
    @property
    def mu(self):
        try:
            outv = self.sum/self.count
        except:
            outv = 0
        return outv
    def generate_values(self):
        while True:
            time.sleep(.1)  # an artificial delay
            yield gauss(0,1)
    def monitor(self, report_interval=1):
        print ("Starting data stream...")
        for x in self.generate_values():
            self.sum   += x
            self.count += 1 

stream = MyStreamMonitor()

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
            while True:
                yield "data: %s %d\n\n" % (stream.count, stream.mu)
                time.sleep(.01) # artificial delay. would rather push whenever values are updated. 
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index.html'))

if __name__ == "__main__":
    # Data monitor should start as soon as the app is started.
    t = threading.Thread(target=stream.monitor)
    t.start()
    print ("Starting webapp...")
    app.run(host='localhost', port=23423)