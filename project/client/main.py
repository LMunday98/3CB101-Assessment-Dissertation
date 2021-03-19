import threading
from multi_client import MultiClient

clients = []
threads = []

# create clients and threads
for index in range(4):
    new_client = MultiClient(index)
    clients.append(new_client)

for client in clients:
    threads.append(threading.Thread(target=client.run))

for thread in threads:
    thread.setDaemon(True)

for thread in threads:
    thread.start()

try:
    input("Press enter to shutdown server")
except Exception as e:
    print("Force quit")

for client in clients:
    client.finish()