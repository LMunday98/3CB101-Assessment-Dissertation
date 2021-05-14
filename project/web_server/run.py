import threading

def thread_flask_server():
    print("\nStart Flask Server\n")
    flask_thread = threading.Thread(target=app.run(host=socket_ip, port=4444))
    flask_thread.setDaemon(True)
    flask_thread.start()

if __name__ == '__main__':
    
    from app import app
    import app.routes.web
    from app.routes.api import *

    try:
        thread_flask_server()
    except Exception as e:
        print(e)

    print("\nExiting")
        
    server_manager_instance.finish()