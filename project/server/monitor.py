import time
import csv

class MyStreamMonitor(object):
    def get_boat_data(self):
        f1 = open("data/session_data.csv", "r")
        last_line = f1.readlines()[-1]
        f1.close()
        row = last_line.split(',')
        return row