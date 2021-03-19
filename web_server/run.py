# run.py
import threading
from app import app

if __name__ == '__main__':

    # Import web and api routes before running the app
    # to prevent circular dependencies
    from app.routes import *
    from app.routes.web import stream
    import 3CB101-Pi.server.multi-server  

    # Start threads
    monitor_thread = threading.Thread(target=stream.monitor)
    monitor_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='cs2s.yorkdc.net', port=5018)