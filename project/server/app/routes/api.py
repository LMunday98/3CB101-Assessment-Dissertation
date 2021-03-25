import time

from app import app
from server_manager import ServerManager
from flask import Flask, Response, request, render_template, redirect

global server_manager_instance
server_manager_instance = ServerManager()
server_manager_instance.setup()
server_manager_instance.start()

@app.route('/stream')
def stream():
    socket_instance = server_manager_instance.get_socket_instance()
    return Response(socket_instance.get_stream(), mimetype="text/event-stream")

@app.route('/socket_call')
def socket_call():
    socket_code = request.args.get('socket_code', None)
    if socket_code != None:
        socket_instance = server_manager_instance.get_socket_instance()
        socket_instance.send_message(socket_code)
    return redirect("/")