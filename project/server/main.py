import threading
from multi_server import MultiServer

multi_server = MultiServer()

listen_thread = threading.Thread(target=multi_server.run_listen)
process_thread = threading.Thread(target=multi_server.run_calc_timing)

listen_thread.setDaemon(True)
process_thread.setDaemon(True)

listen_thread.start()
process_thread.start()

try:
    input("Press enter to shutdown server")
except Exception as e:
    print("Force quit")

multi_server.finish()