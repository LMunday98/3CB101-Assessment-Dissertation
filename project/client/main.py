import threading
from multi_client import MultiClient
from mpu.sensor import Sensor

num_clients = 1
single_client_index = 0
clients = []
threads = []

def create_sensor(rower_index):
    return Sensor(rower_index)

def create_client(new_index, sensor):
    clients.append(MultiClient(new_index, sensor))

def create_single(index, sensor):
    create_client(index, sensor)

def create_multi(num_clients, sensor):
    # create clients and threads
    for index in range(num_clients):
        create_client(index, sensor)

def run_client(single_client_index, sensor):
    if num_clients == 1:
        create_single(single_client_index, sensor)
    else:
        create_multi(num_clients, sensor)

    for client in clients:
        threads.append(threading.Thread(target=client.run))

    for thread in threads:
        thread.setDaemon(True)

    for thread in threads:
        thread.start()

    print ("Clients", clients)
    print ("Threads", threads)

    try:
        input("Press enter to shutdown server")
    except Exception as e:
        print("Force quit")

    for client in clients:
        client.finish()

sensor = create_sensor(single_client_index)
run_client(single_client_index, sensor)