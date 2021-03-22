import time
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context
from app import app

from monitor import MyStreamMonitor

stream = MyStreamMonitor()

def get_data(stream):
    time.sleep(.2)
    data_stream = stream.get_data_string()
    return data_stream

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/stream')
def stream():
    stream = MyStreamMonitor()
    @stream_with_context
    def eventStream():
        while True:
            yield 'data: %s\n\n' % (get_data(stream))
    return Response(eventStream(), mimetype="text/event-stream")