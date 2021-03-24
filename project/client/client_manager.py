import socket, threading
from multi_client import MultiClient

class ClientManager:
    def __init__(self):
        self.clients = []
        self.threads = []
        self.rower_index = self.get_rower_index()
        self.create_new_client(self.rower_index)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
        
    def get_rower_index(self):
        ip_dict = {
            "192.168.0.184" : -1, # Host
            "192.168.0.186" : 0,  # Bow
            "192.168.0.162" : 1,  # Bow 2
            "192.168.0.178" : 2,  # Stroke 2
            "192.168.0.120" : 3   # Stroke
        }

        ip = self.get_ip()
        return ip_dict[ip]

    def create_new_client(self, rower_index):
        self.clients.append(MultiClient(rower_index))

    def thread_clients(self):
        for client in self.clients:
            self.threads.append(threading.Thread(target=client.run))

        for thread in self.threads:
            thread.setDaemon(True)

    def start_threads(self):
        for thread in self.threads:
            thread.start()

    def finish_threads(self):
        try:
            input("Press enter to shutdown client\n")
        except Exception as e:
            print("Force quit")

        for client in self.clients:
            client.finish()

    def run(self):
        self.thread_clients()
        self.start_threads()
        self.finish_threads()