import threading

# flask
from app import app
from app.routes import *

# server
from multi_server import MultiServer
multi_server = MultiServer()

def socket_server():
    print("\nStart Socket Server")
    listen_thread = threading.Thread(target=multi_server.run_listen)
    process_thread = threading.Thread(target=multi_server.run_calc_timing)

    listen_thread.setDaemon(True)
    process_thread.setDaemon(True)

    listen_thread.start()
    process_thread.start()

def flask_server():
    print("\nStart Flask Server\n")
    flask_thread = threading.Thread(target=app.run(host='192.168.0.184', port=4444))
    flask_thread.setDaemon(True)
    flask_thread.start()


if __name__ == '__main__':

    try:
        socket_server()
    except Exception as e:
        print(e)

    try:
        flask_server()
    except Exception as e:
        print(e)

    print("\nExiting")

    multi_server.finish()