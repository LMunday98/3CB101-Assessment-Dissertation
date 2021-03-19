import time
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context
from app import app

from monitor import MyStreamMonitor

stream = MyStreamMonitor()

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/stream')
def stream():
    @stream_with_context
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")