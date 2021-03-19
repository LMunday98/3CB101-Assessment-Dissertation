import time

class MyStreamMonitor(object):
    def __init__(self):
        self.count = 0
    def monitor(self, report_interval=1):
        while True:
            print('class count', self.count)
            self.count += 1 
            time.sleep(.5)
    def get_count(self):
        return self.count