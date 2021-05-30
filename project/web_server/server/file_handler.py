from shutil import copyfile
from datetime import datetime
import json, os

class FileHandler:
    def __init__(self):
        self.record_session = False
        self.access_rights = 0o755

        realtime = {
            'path' : 'data/realtime/',
            'file_name' : 'session_data.csv',
            'write_mode' : 'a'
        }

        copy = {
            'path' : 'data/saved_sessions/'
        }

        self.file_details = {'realtime' : realtime, 'copy' : copy}
        self.setup()

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

    def write_rower_data(self, write_type, data_string):
        write_details = self.file_details[write_type]
        f = open(write_details['path'] + write_details['file_name'], write_details['write_mode'])
        f.write(data_string)
        f.close()

    def set_session_status(self, record_session):
        if (not record_session):
            realtime = self.file_details['realtime']
            copy = self.file_details['copy']
            copyfile(realtime['path'] + realtime['file_name'], copy['path'] + self.get_session_name())
            os.remove(realtime['path'] + realtime['file_name'])
        self.record_session = record_session

    def get_session_name(self):
        return 'session_data ' + str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + '.csv'

    def record_data(self, rower_data):
        if (self.record_session):
            json_string = json.dumps(rower_data[0]) + json.dumps(rower_data[1]) + json.dumps(rower_data[2]) + json.dumps(rower_data[3]) + '\n'
            self.write_rower_data('realtime', json_string)