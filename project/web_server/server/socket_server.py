import sys, time, datetime, socket, traceback, select
from file_handler import FileHandler
from connection_handler import ConnectionHandler

# sys.path.append("..")
# import mpu

class SocketServer:
    def __init__(self):
        self.buffer = 4096
        self.port = 5001
        self.local_ip = self.get_ip()
        self.create_socket()
    
    def create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.server_socket.bind((self.local_ip, self.port))
                self.server_socket.listen(10)
                break
            except Exception as e:
                print("Couldnt create socket server\t", e, "\t", datetime.datetime.now().time().strftime('%H:%M:%S'))
            time.sleep(1)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception as e:
            print(e)
            print(ip)
        finally:
            s.close()
        return ip
        
    def setup(self):
        # Add server socket to the list of readable connections
        self.connection_handler = ConnectionHandler(self.server_socket, self.buffer, self.local_ip)

        # Setup server handlers
        self.file_handler = FileHandler()
        self.data_handler = self.connection_handler.get_data_handler()

        # Runtime vars
        self.run_server = True
        self.session_name = datetime.datetime.now()

    def run_listen(self):
        print ("\33[32m \t\t\t\tSocket Server Running \33[0m")
        while self.run_server:
            self.connection_handler.check_connections()
        # Close socket
        try:
            self.connection_handler.disconnect_all()
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except Exception as e:
            # print(e)
            x = 1

    def run_send(self):
        while self.run_server:
            try:
                #print('Request data')
                self.connection_handler.send_to_all('send_data')
            except Exception as e:
                # print('Error requesting sensor data')
                x=1
            time.sleep(.1)

    def record_data(self):
        while self.run_server:
            try:
                self.file_handler.record_data(self.data_handler.get_rower_dicts())
            except Exception as e:
                print(e)
                # x=1
            time.sleep(.1)
            
    def finish(self):
        print("Closing socket")
        self.run_server = False

    def get_latest_data(self, rower_index):
        return self.data_handler.get_rower_json(int(rower_index))

    def server_request(self, socket_code):
        if socket_code == "session_start":
            print("Start session")
            self.file_handler.set_session_status(True)
        elif socket_code == "session_end":
            print("End session")
            self.file_handler.set_session_status(False)
        elif socket_code == "disconnect_all":
            print("Disconnect clients")
            self.connection_handler.disconnect_all(socket_code)
        else:
            self.connection_handler.send_to_all(socket_code)