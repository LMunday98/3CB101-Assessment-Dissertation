import socket, select, string, sys, time, pickle
from connection_handler import ConnectionHandler
sys.path.append("..")
from mpu.sensor import Sensor

class SocketClient:
    def __init__(self, client_index):
        self.run_client = True
        self.client_index = client_index
        self.connection_handler = ConnectionHandler(str(client_index))

    def setup_sensor(self):
        while True:
            try:
                self.sensor = Sensor(self.client_index)
                print ("\33[32m\33[1mSuccessfully setup sensor \33[0m")
                break
            except Exception as e:
                print ("\33[31m\33[1mError setting up the sensor \33[0m")
                time.sleep(1)    

    def read_sensor(self):
        try:
            sensor_data = self.sensor.get_data()
            message = pickle.dumps(sensor_data)
            # print(data_string)
            self.connection_handler.send_message(message)
        except:
            print ("\n\33[93m\33[1mReinitalising sensor \33[0m")
            self.setup_sensor()
        
    def send(self):
        while self.run_client:
            try:
                self.read_sensor()
                time.sleep(.2)
            except Exception as e:
                print (e)
                    
    def listen(self):
        while self.run_client:
            socket_code = self.connection_handler.connection_listen()
            self.execute_code(socket_code)
            
    def execute_code(self, socket_code):
        if socket_code == "cal":
            print("Calibration call")
            self.sensor.calibrate()
        if socket_code == "disconnect_all":
            print("Disconnecting client")
            # self.connection_handler.close_socket()

    def finish(self):
        sys.exit()
