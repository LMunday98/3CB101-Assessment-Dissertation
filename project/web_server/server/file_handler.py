class FileHandler:
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

    def write_rower_data(self, file_dir, file_name, data_to_write, file_method="a"):
        f = open("data/" + file_dir + file_name + ".csv", file_method)
        data_string = "\n"
        if file_method == "w":
            data_string = ""
        for data in data_to_write:
            data_string = data_string + str(data) + ","
        data_string = data_string[:-1]
        f.write(data_string)
        f.close()

    def get_csv_to_json(self):
        return {'Stroke': 100, 'Stroke2': 200, 'Bow2': 300, 'Bow': 400}