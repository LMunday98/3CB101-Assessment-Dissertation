import threading
from socket_server_package.socket_server import SocketServer

class ServerManager:
    def __init__(self):
        self.socket_server = SocketServer()

    def setup(self):
        self.threads = []
        self.socket_server.setup()
        listen_thread = threading.Thread(target=self.socket_server.run_listen)
        process_thread = threading.Thread(target=self.socket_server.run_calc_timing)

        listen_thread.setDaemon(True)
        process_thread.setDaemon(True)

        self.threads.append(listen_thread)
        self.threads.append(process_thread)

    def start(self):
        for thread in self.threads:
            thread.start()

    def finish(self):
        self.socket_server.finish()

    def get_socket_instance(self):
        return self.socket_server