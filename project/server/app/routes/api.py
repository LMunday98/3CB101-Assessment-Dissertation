import time

from app import app
from server_manager import ServerManager
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context

global server_manager_instance
server_manager_instance = ServerManager()
server_manager_instance.setup()
server_manager_instance.start()

@app.route('/stream')
def stream():
    socket_instance = server_manager_instance.get_socket_instance()
    return Response(socket_instance.get_stream(), mimetype="text/event-stream")