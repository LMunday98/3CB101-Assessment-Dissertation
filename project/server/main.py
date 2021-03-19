import threading
from multi_server import MultiServer

multi_server = MultiServer()
server_thread = threading.Thread(target=multi_server.run)
server_thread.setDaemon(True)
server_thread.start()

try:
    input("Press enter to shutdown server")
except Exception as e:
    print("Force quit")

multi_server.finish()