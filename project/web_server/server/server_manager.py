import threading
from server.socket_server import SocketServer

class ServerManager:
    def __init__(self):
        self.socket_server = SocketServer()
        self.threads = []
        self.socket_ip = self.socket_server.get_ip()

    def create_thread(self, thread_target):
        print('Create thread')
        new_thread = threading.Thread(target=thread_target)
        self.threads.append(new_thread)

    def setup(self):
        print('Socket setup')
        self.socket_server.setup()
        self.create_thread(self.socket_server.run_listen)
        self.create_thread(self.socket_server.run_send)

        print('Set dameon')
        for thread in self.threads:
            thread.setDaemon(True)

    def start(self):
        for thread in self.threads:
            print('Start thread')
            thread.start()

    def finish(self):
        self.socket_server.finish()

    def get_socket_instance(self):
        return self.socket_server

    def get_socket_ip(self):
        return self.socket_ip