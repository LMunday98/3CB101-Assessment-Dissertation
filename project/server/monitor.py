import time

class MyStreamMonitor(object):
    def __init__(self):
        self.boat_data = {
            "stroke" : 0,
            "seat2" : 0,
            "seat3" : 0,
            "seat4" : 0
        }
    def monitor(self, report_interval=1):
        while True:
            # print(self.boat_data)
            self.boat_data["stroke"] += 1
            self.boat_data["seat2"] += 1
            self.boat_data["seat3"] += 1
            self.boat_data["seat4"] += 1
            time.sleep(.1)
    def get_boat_data(self):
        return self.boat_data