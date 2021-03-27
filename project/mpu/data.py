import datetime
from .calcs import Calc

class Data:

    rowerId = 0

    def __init__(self, rowerId, gx, gy, gz, ax, ay, az, cal_offset, data_datetime):
        self.rowerId = rowerId

        self.gx = gx
        self.gy = gy
        self.gz = gz

        self.sgx = (gx / 131)
        self.sgy = (gy / 131)
        self.sgz = (gz / 131)

        self.ax = ax
        self.ay = ay
        self.az = az

        sax = (ax / 16384.0)
        say = (ay / 16384.0)
        saz = (az / 16384.0)

        self.sax = sax
        self.say = say
        self.saz = saz

        calculations = Calc()

        self.rx = calculations.get_x_rotation(sax, say, saz) - cal_offset[0]
        self.ry = calculations.get_y_rotation(sax, say, saz) - cal_offset[0]

        self.data_datetime = data_datetime

    def set_rowerId(self, newId):
        self.rowerId = newId

    def get_rowerId(self):
        return self.rowerId

    def get_data_datetime(self):
        return self.data_datetime

    def get_all_data(self):
        return [self.rowerId, self.gx, self.gy, self.gz, self.sax, self.say, self.saz, self.rx, self.ry, self.data_datetime]

    def get_sensor_dict(self):
        return {'gx' : self.gx, 'gy' : self.gy, 'gz' : self.gz, 'sax' : self.sax, 'say' : self.say, 'saz' : self.saz, 'rx' : self.rx, 'ry' : self.ry}

    def get_sensor_data(self):
        return [self.gx, self.gy, self.gz, self.sax, self.say, self.saz, self.rx, self.ry]

    def printData(self):
        print ("\nRower Identification")
        print ("Id: ", ("%5d" % self.rowerId))

        print ("\nGyroscope")
        print ("gyro_xout: ", ("%5d" % self.gx), " scaled: ", self.sgx)
        print ("gyro_yout: ", ("%5d" % self.gy), " scaled: ", self.sgy)
        print ("gyro_zout: ", ("%5d" % self.gz), " scaled: ", self.sgz)

        print ("\nAcceleromoter")
        print ("accel_xout: ", ("%6d" % self.ax), " scaled: ", self.sax)
        print ("accel_yout: ", ("%6d" % self.ay), " scaled: ", self.say)
        print ("accel_zout: ", ("%6d" % self.az), " scaled: ", self.saz)

        print ("\nRotation")
        print ("X Rotation: " , self.rx)
        print ("Y Rotation: " , self.ry)

        print ("\n- - - - - - - - - - - - - -")