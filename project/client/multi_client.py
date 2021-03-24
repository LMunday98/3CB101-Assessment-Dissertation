import socket, select, string, sys
import time
import random
import pickle

import sys
sys.path.append("..")
from mpu.sensor import Sensor

class MultiClient:
    def __init__(self, client_index):
        self.run_client = True
        self.name = str(client_index)
        self.sensor = Sensor(client_index)
        self.port = 5001

        if len(sys.argv)<2:
            self.host = '192.168.0.184'
        else:
            self.host = sys.argv[1]
            
    def establish_connection(self):
        # connecting host
        try :
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(2)
            self.s.connect((self.host, self.port))
            self.s.send(self.name.encode())
            print ("\33[32m\33[1mSuccessfully connected to the server \33[0m")
        except :
            print ("\33[31m\33[1mCan't connect to the server \33[0m")

    def run(self):
        while self.run_client:
            try:
                sensor_data = self.sensor.get_data()
                data_string = pickle.dumps(sensor_data)
                self.s.send(data_string)
                time.sleep(.2)
            except Exception as e:
                print (e)
                print ("\n\33[93m\33[1mReconnecting to server \33[0m")
                self.establish_connection()
                time.sleep(1)

    def finish(self):
        try:
            self.s.send("tata ".encode())
        except Exception as e:
            print(e)
        sys.exit()
