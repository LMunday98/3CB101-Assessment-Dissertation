import time
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context
from app import app

from monitor import MyStreamMonitor

@app.route('/stream')
def stream():
    stream = MyStreamMonitor()
    return Response(stream.get_stream(), mimetype="text/event-stream")