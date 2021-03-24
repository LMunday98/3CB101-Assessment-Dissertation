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

        if len(sys.argv)<2:
            # host = input("Enter host ip address: ")
            self.host = '192.168.0.184'
        else:
            self.host = sys.argv[1]

        self.port = 5001



        #self.establish_connection()

    def establish_connection(self):
        # connecting host
        try :
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.settimeout(2)
            self.s.connect((self.host, self.port))
            #if connected
            self.s.send(self.name.encode())
        except :
            print ("\33[31m\33[1m Can't connect to the server \33[0m")
            # sys.exit()

        

    def run(self):
        while self.run_client:
            try:
                socket_list = [sys.stdin, self.s]
                sensor_data = self.sensor.get_data()
                sensor_data.printData()
                print(str(sensor_data.get_data_datetime()))
                data_string = pickle.dumps(sensor_data)
                self.s.send(data_string)
                time.sleep(.2)
            except Exception as e:
                print (e)
                print ("RECONNECTING")
                self.establish_connection()
                time.sleep(1)

    def finish(self):
        self.s.send("tata ".encode())
        sys.exit()
