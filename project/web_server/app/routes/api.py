import time, sys
from app import app
sys.path.append('/home/pi/Documents/3CB101-Pi/project/web_server/server')
sys.path.append("server")
from server_manager import ServerManager
from flask import Flask, Response, request, render_template, redirect

global server_manager_instance
server_manager_instance = ServerManager()
server_manager_instance.setup()
server_manager_instance.start()

socket_ip = server_manager_instance.get_socket_ip()

@app.route('/socket_call')
def socket_call():
    socket_instance = server_manager_instance.get_socket_instance()
    socket_code = request.args.get('socket_code', None)
    if socket_code == "get_data":
        print('api call: ', get_data())
    elif socket_code != None:
        socket_instance.server_request(socket_code)
    return redirect("/public/test")

@app.route('/get_data')
def get_data():
    rower_index = request.args.get('rower_index', '0')
    code_string = request.args.get('code', None)
    socket_instance = server_manager_instance.get_socket_instance()
    latest_data = socket_instance.get_latest_data(rower_index)
    return latest_data