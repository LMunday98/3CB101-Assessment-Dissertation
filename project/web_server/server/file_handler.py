from shutil import copyfile
from datetime import datetime
import json, os

class FileHandler:
    def __init__(self):
        self.record_session = False
        self.session_name = ''
        self.access_rights = 0o755

        realtime = {
            'path' : 'data/realtime/',
            'file_name' : 'session_data.csv',
            'write_mode' : 'a'
        }

        copy = {
            'path' : 'data/saved_sessions/',
            'file_name' : self.session_name,
            'write_mode' : 'w'
        }

        self.file_details = {'realtime' : realtime, 'copy' : copy}
        self.setup()
        # copyfile("data/realtime_analysis/session_data.csv", "data/captured_analysis/session_data_" + str(self.session_name) + ".csv")

    def setup(self):
        self.create_dir('data')
        for key in self.file_details:
            path = self.file_details[key]['path']
            self.create_dir(path)
            

    def create_dir(self, path):
        try:
            os.mkdir(path, self.access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

    def write_rower_data(self, file_dir, file_name, data_to_write, file_method="a"):
        f = open("data/" + file_dir + file_name + ".csv", file_method)
        f.write(data_string)
        f.close()

    def set_session_status(self, record_session):
        if (record_session):
            self.session_name = str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        self.record_session = record_session

    def record_data(self, rower_data):
        if (self.record_session):
            json_string = json.dumps(rower_data[0]) + json.dumps(rower_data[1]) + json.dumps(rower_data[2]) + json.dumps(rower_data[3])
            self.write_rower_data('realtime/', self.session_name, json_string)