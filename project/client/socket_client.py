import socket, select, string, sys, time, pickle
from connection_handler import ConnectionHandler
print(str(sys.path))
print("\n\n\n")
sys.path.append('/home/pi/Documents/3CB101-Pi/project/mpu')
print(str(sys.path))
print("\n\n\n")
from sensor import Sensor

class SocketClient:
    def __init__(self, client_index):
        self.run_client = True
        self.client_index = client_index
        self.connection_handler = ConnectionHandler(str(client_index))

    def setup(self):
        self.connection_handler.socket_create()
        self.connection_handler.socket_connect()
        self.setup_sensor()

    def setup_sensor(self):
        while True:
            try:
                self.sensor = Sensor(self.client_index)
                print ("\33[32m\33[1mSuccessfully setup sensor \33[0m")
                break
            except Exception as e:
                print ("\33[31m\33[1mError setting up the sensor \33[0m")
                print (e)
                time.sleep(1)

    def read_sensor(self):
        try:
            sensor_data = self.sensor.get_data()
            return pickle.dumps(sensor_data)
        except Exception as e:
            print ("\n\33[93m\33[1mReinitalising sensor \33[0m")
            print (e)
            self.setup_sensor()

    def send(self):
        try:
            print("Send to server")
            pickle_data = self.read_sensor()
            self.connection_handler.socket_send(pickle_data)
        except Exception as e:
            print (e)

    def listen(self):
        self.setup()
        while self.run_client:
            socket_code = self.connection_handler.connection_listen()
            self.execute_code(socket_code)

    def execute_code(self, socket_code):
        if socket_code == "send_data":
            self.send()
        elif socket_code == "calibrate":
            print("Calibration call")
            self.sensor.calibrate()
        elif socket_code == "disconnect_all":
            print("Disconnecting client")
            self.connection_handler.socket_reconnect()

    def finish(self):
        sys.exit()
