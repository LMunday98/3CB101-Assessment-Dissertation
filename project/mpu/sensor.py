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
            'rx' : 0,
            'ry' : 0
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

    def calibrate(self):
        print("Calibrating sensor...")
        calibration_reading = self.get_data().get_data_dict()
        self.calibration_offsets['rx'] = self.calibration_offsets['rx'] + calibration_reading['rx']
        self.calibration_offsets['ry'] = self.calibration_offsets['ry'] + calibration_reading['ry']
        print(self.calibration_offsets)

    def get_data(self):
        gyro = {
            'gx' : self.read_word_2c(self.GYRO_X),
            'gy' : self.read_word_2c(self.GYRO_Y),
            'gz' : self.read_word_2c(self.GYRO_Z)
        }

        accel = {
            'ax' : self.read_word_2c(self.ACCEL_X),
            'ay' : self.read_word_2c(self.ACCEL_Y),
            'az' : self.read_word_2c(self.ACCEL_Z)
        }

        return Data(self.rowerId, { 'gyro' : gyro, 'accel' : accel }, self.calibration_offsets)