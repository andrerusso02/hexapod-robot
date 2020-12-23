#import serial
from math import *
from util import *

#ser = serial.Serial('/dev/serial0', 57600)

def send_pos(id, angle_rad, delay_sec):
    #global ser
    min = [932, 987, 929, 875, 1018, 904, 982, 963, 938, 98, 70, 36, 128, 58, 79, 93, 33, 96]
    max = [58, 113, 55, 1, 144, 30, 108, 89, 64, 972, 944, 910, 1002, 932, 953, 967, 907, 970]
    angle_10b = int(mapf(angle_rad, 0, pi, min[id - 1], max[id - 1]))
    #ser.write("M".encode("ascii"))
    #ser.write(chr(id).encode("ascii"))
    #ser.write(angle_10b.to_bytes(2, 'little'))
    #ser.write(to_milis(delay_sec).to_bytes(2, 'little'))


def read_batt():
    ser.write("B".encode("ascii"))
    batt = int.from_bytes(ser.read(), byteorder='big')
    return batt