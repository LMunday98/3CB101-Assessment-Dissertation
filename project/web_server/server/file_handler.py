from shutil import copyfile
from datetime import datetime
import json, os

class FileHandler:
    def __init__(self):
        self.record_session = True
        self.access_rights = 0o755

        root = '/home/pi/Documents/3CB101-Pi/project/data'

        data = {
            'path' : root
        }

        realtime = {
            'path' : root + '/realtime/',
            'file_name' : 'session_data.csv',
            'write_mode' : 'a'
        }

        copy = {
            'path' : root + '/saved_sessions/'
        }

        self.file_details = {'data': data, 'realtime' : realtime, 'copy' : copy}
        self.setup()

    def setup(self):
        for key in self.file_details:
            path = self.file_details[key]['path']
            self.create_dir(path)

    def create_dir(self, path):
        try:
            print("Creating", path)
            os.mkdir(path, self.access_rights)
        except Exception as e:
            print (e)
        else:
            print ("Successfully created the directory %s" % path)

    def write_rower_data(self, write_type, data_string):
        write_details = self.file_details[write_type]
        f = open(write_details['path'] + write_details['file_name'], write_details['write_mode'])
        f.write(data_string)
        f.close()

    def set_session_status(self, record_session):
        try:
            if (not record_session):
                realtime = self.file_details['realtime']
                copy = self.file_details['copy']
                copyfile(realtime['path'] + realtime['file_name'], copy['path'] + self.get_session_name())
                os.remove(realtime['path'] + realtime['file_name'])
            self.record_session = record_session
            print(self.record_session)
        except Exception as e:
            print(e)
        

    def get_session_name(self):
        return 'session_data ' + str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + '.csv'

    def record_data(self, rower_data):
        if (self.record_session):
            json_string = json.dumps(rower_data[0]) + json.dumps(rower_data[1]) + json.dumps(rower_data[2]) + json.dumps(rower_data[3]) + '\n'
            self.write_rower_data('realtime', json_string)