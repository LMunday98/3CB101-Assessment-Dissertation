import socket, select, string, sys, time, pickle
sys.path.append("..")
from mpu.sensor import Sensor

class MultiClient:
    def __init__(self, client_index):
        self.run_client = True
        self.name = str(client_index)
        self.client_index = client_index
        self.port = 5001

        if len(sys.argv)<2:
            self.host = '192.168.0.184'
        else:
            self.host = sys.argv[1]

    def setup_sensor(self):
        while True:
            try:
                self.sensor = Sensor(self.client_index)
                print ("\33[32m\33[1mSuccessfully setup sensor \33[0m")
                break
            except Exception as e:
                print ("\33[31m\33[1mError setting up the sensor \33[0m")
                time.sleep(1)

    def establish_connection(self):
        while True:
            try :
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(2)
                self.s.connect((self.host, self.port))
                self.s.send(self.name.encode())
                print ("\33[32m\33[1mSuccessfully connected to the server \33[0m")
                break
            except :
                print ("\33[31m\33[1mCan't connect to the server \33[0m")
                time.sleep(1)

    def read_sensor(self):
        try:
            sensor_data = self.sensor.get_data()
            data_string = pickle.dumps(sensor_data)
            # print(data_string)
            self.send_data(data_string)
        except:
            print ("\n\33[93m\33[1mReinitalising sensor \33[0m")
            self.setup_sensor()

    def send_data(self, data_to_send):
        try:
            self.s.send(data_to_send)
        except:
            print ("\n\33[93m\33[1mReconnecting to server \33[0m")
            self.establish_connection()

    def send(self):
        self.setup_sensor()
        self.establish_connection()
        time.sleep(.2)

        while self.run_client:
            try:
                #print("send")
                self.read_sensor()
                time.sleep(.2)
            except Exception as e:
                print (e)
                    
    def listen(self):
        s = self.s
        while self.run_client:
            #print("listen")
            socket_list = [sys.stdin, s]

            # Get the list of sockets which are readable
            rList, wList, error_list = select.select(socket_list , [], [])

            for sock in rList:
                #incoming message from server
                if sock == s:
                    data = sock.recv(4096)
                    if not data :
                        print ('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
                    else :
                        sys.stdout.write(data.decode())
            

    def finish(self):
        try:
            self.s.send("tata ".encode())
        except Exception as e:
            print(e)
        sys.exit()
