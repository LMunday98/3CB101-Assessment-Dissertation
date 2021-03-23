import time
import csv
from flask import stream_with_context


class MyStreamMonitor(object):
    def read_boat_data(self):
        f1 = open("data/realtime_analysis/session_data.csv", "r")
        last_line = f1.readlines()[-1]
        f1.close()
        row = last_line.split(',')
        return row

    def get_data_string(self):
        data_array = self.read_boat_data()
        data_string = ','.join(data_array)
        return data_string

    @stream_with_context
    def get_stream(self):
        while True:
            time.sleep(.2)
            yield 'data: %s\n\n' % (self.get_data_string())