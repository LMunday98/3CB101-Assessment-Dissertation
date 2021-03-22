import threading
from multi_client import MultiClient

num_clients = 4
single_client_index = 0
clients = []
threads = []

def create_client(new_index):
    clients.append(MultiClient(new_index))

def create_single(index):
    create_client(index)

def create_multi(num_clients):
    # create clients and threads
    for index in range(num_clients):
        create_client(index)

def run(single_client_index):
    if num_clients == 1:
        create_single(single_client_index)
    else:
        create_multi(num_clients)

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

run(single_client_index)
