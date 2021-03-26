import time

from app import app
from server.server_manager import ServerManager
from flask import Flask, Response, request, render_template, redirect

global server_manager_instance
server_manager_instance = ServerManager()
server_manager_instance.setup()
server_manager_instance.start()

@app.route('/socket_call')
def socket_call():
    socket_code = request.args.get('socket_code', None)
    if socket_code != None:
        socket_instance = server_manager_instance.get_socket_instance()
        socket_instance.send_message(socket_code)
    return redirect("/")

@app.route('/get_data')
def get_data():
    code_string = request.args.get('code', None)
    socket_instance = server_manager_instance.get_socket_instance()
    latest_data = socket_instance.get_latest_data()
    return latest_data