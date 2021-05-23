import sys
import time
print("- " * 10)
# time.sleep(15)
time.sleep(1)
sys.path.append('/home/pi/Documents/3CB101-Pi/project/client')
from client_manager import ClientManager

manager = ClientManager()
manager.run()
