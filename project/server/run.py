# run.py
import threading

if __name__ == '__main__':

    # Import web and api routes before running the app
    # to prevent circular dependencies
    from app import app
    from app.routes import *
    
    app.run(host='192.168.0.184', port=5000)
    #app.run(host='cs2s.yorkdc.net', port=5018)