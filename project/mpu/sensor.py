import smbus
import time
import datetime
import math
from data import Data

class Sensor():

    # Mpu 6050 registers

    MPU_6050_ADDR   = 0x68
    PWR_MGMT_1      = 0x6b
    GYRO_X          = 0x43
    GYRO_Y          = 0x45
    GYRO_Z          = 0x47
    ACCEL_X         = 0x3b
    ACCEL_Y         = 0x3d
    ACCEL_Z         = 0x3f

    def __init__(self, rowerId):
        self.rowerId = rowerId
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.MPU_6050_ADDR, self.PWR_MGMT_1, 0)
        self.calibration_offsets = {
            'x_offset' : 0,
            'y_offset' : 0
        }

    def read_byte(self, reg):
        return self.bus.read_byte_data(self.MPU_6050_ADDR, reg)
 
    def read_word(self, reg):
        h = self.bus.read_byte_data(self.MPU_6050_ADDR, reg)
        l = self.bus.read_byte_data(self.MPU_6050_ADDR, reg + 1)
        value = (h << 8) + l
        return value
    
    def read_word_2c(self, reg):
        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
    
    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))
    
    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)
    
    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

    def calibrate(self):
        print("Calibrating sensor...")

    def get_data(self):
        gyro = {
            'gx' : self.read_word_2c(self.GYRO_X),
            'gy' : self.read_word_2c(self.GYRO_Y),
            'gz' : self.read_word_2c(self.GYRO_Z)
        }

        scaled_gyro = {
            'sgx' : gyro['gx'] / 131,
            'sgy' : gyro['gy'] / 131,
            'sgz' : gyro['gz'] / 131
        }

        accel = {
            'ax' : self.read_word_2c(self.ACCEL_X),
            'ay' : self.read_word_2c(self.ACCEL_Y),
            'az' : self.read_word_2c(self.ACCEL_Z)
        }

        scaled_accel = {
            'sax' : accel['ax'] / 16384.0,
            'say' : accel['ay'] / 16384.0,
            'saz' : accel['az'] / 16384.0
        }

        rotation = {
            'rx' : self.get_x_rotation(scaled_accel['sax'], scaled_accel['say'], scaled_accel['saz']),
            'ry' : self.get_y_rotation(scaled_accel['sax'], scaled_accel['say'], scaled_accel['saz'])
        }

        sensor_readings = {
            'gyro' : gyro,
            'scaled_gyro' : scaled_gyro,
            'accel' : accel,
            'scaled_accel' : scaled_accel,
            'rotation' : rotation
        }

        print ("gyro")
        print ("--------")
        
        print ("gyro_xout: ", ("%5d" % gyro['gx']), " scaled: ", (scaled_gyro['sgx']))
        print ("gyro_yout: ", ("%5d" % gyro['gy']), " scaled: ", (scaled_gyro['sgy']))
        print ("gyro_zout: ", ("%5d" % gyro['gz']), " scaled: ", (scaled_gyro['sgz']))
        
        print
        print ("accelerometer")
        print ("---------------------")
        
        print ("accel_xout: ", ("%6d" % accel['ax']), " scaled: ", scaled_accel['sax'])
        print ("accel_yout: ", ("%6d" % accel['ay']), " scaled: ", scaled_accel['say'])
        print ("accel_zout: ", ("%6d" % accel['az']), " scaled: ", scaled_accel['saz'])
        
        print ("X Rotation: " , rotation['rx'])
        print ("Y Rotation: " , rotation['ry'])

        data = Data(self.rowerId, sensor_readings, self.calibration_offsets)
        return data