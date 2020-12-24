import time
import serial

import util
from math import pi

startByte = 0xFF
TIMEOUT = 600  # TIMEOUT 600

# register Address
P_VERSION_L = 3
P_VERSION_H = 4
P_ID = 5
dP_BAUD_RATE = 6
P_RETURN_DELAY_TIME = 7
P_RETURN_LEVEL = 8
P_MIN_ANGLE_LIMIT_L = 9
P_MIN_ANGLE_LIMIT_H = 10
P_MAX_ANGLE_LIMIT_L = 11
P_MAX_ANGLE_LIMIT_H = 12
P_LIMIT_TEMPERATURE = 13
P_MAX_LIMIT_VOLTAGE = 14
P_MIN_LIMIT_VOLTAGE = 15
P_MAX_TORQUE_L = 16
P_MAX_TORQUE_H = 17
P_ALARM_LED = 19
P_ALARM_SHUTDOWN = 20
P_COMPLIANCE_P = 21
P_PUNCH_L = 24
P_PUNCH_H = 25
P_CW_DEAD = 26
P_CCW_DEAD = 27

P_TORQUE_ENABLE = 40
P_LED = 41
P_GOAL_POSITION_L = 42
P_GOAL_POSITION_H = 43
P_GOAL_TIME_L = 44
P_GOAL_TIME_H = 45
P_GOAL_SPEED_L = 46
P_GOAL_SPEED_H = 47
P_LOCK = 48
P_PRESENT_POSITION_L = 56
P_PRESENT_POSITION_H = 57
P_PRESENT_SPEED_L = 58
P_PRESENT_SPEED_H = 59
P_PRESENT_LOAD_L = 60
P_PRESENT_LOAD_H = 61
P_PRESENT_VOLTAGE = 62
P_PRESENT_TEMPERATURE = 63
P_REGISTERED_INSTRUCTION = 64
P_MOVING = 66

# Instruction:
INST_PING = 0x01
INST_READ = 0x02
INST_WRITE = 0x03
INST_REG_WRITE = 0x04
INST_ACTION = 0x05
INST_RESET = 0x06
INST_SYNC_WRITE = 0x83

minPos10b = [932, 987, 929, 875, 1018, 904, 982, 963, 938, 98, 70, 36, 128, 58, 79, 93, 33, 96]
maxPos10b = [58, 113, 55, 1, 144, 30, 108, 89, 64, 972, 944, 910, 1002, 932, 953, 967, 907, 970]

ser = serial.Serial('/dev/serial0', 1000000)

byteOrder = 'little'


def enableTorque(idServo):
    global ser

    enableT = 1
    messageLength = 4

    ser.write(startByte.to_bytes(1, byteOrder))
    ser.write(startByte.to_bytes(1, byteOrder))
    ser.write(idServo.to_bytes(1, byteOrder))
    ser.write(messageLength.to_bytes(1, byteOrder))
    ser.write(INST_WRITE.to_bytes(1, byteOrder))
    ser.write(P_TORQUE_ENABLE.to_bytes(1, byteOrder))
    ser.write(enableT.to_bytes(1, byteOrder))
    ser.write(((~(idServo + messageLength + INST_WRITE + enableT + P_TORQUE_ENABLE)) & 0xFF).to_bytes(1, byteOrder))


def writePos(idServo, posRad, timeSec):
    global ser, minPos10b, maxPos10b
    angle10b = int(util.mapf(posRad, 0, pi, minPos10b[idServo - 1], maxPos10b[idServo - 1]))
    timeMilis = util.to_milis(timeSec)

    messageLength = 7
    posH, posL = angle10b.to_bytes(2, 'little')
    timH, timL = timeMilis.to_bytes(2, 'little')

    ser.write(startByte.to_bytes(1, byteOrder))
    ser.write(startByte.to_bytes(1, byteOrder))
    ser.write(idServo.to_bytes(1, byteOrder))
    ser.write(messageLength.to_bytes(1, byteOrder))
    ser.write(INST_WRITE.to_bytes(1, byteOrder))
    ser.write(P_GOAL_POSITION_L.to_bytes(1, byteOrder))
    ser.write(posL.to_bytes(1, byteOrder))
    ser.write(posH.to_bytes(1, byteOrder))
    ser.write(timL.to_bytes(1, byteOrder))
    ser.write(timH.to_bytes(1, byteOrder))
    ser.write(((~(idServo + messageLength + INST_WRITE + P_GOAL_POSITION_L + posL + posH + timL + timH)) & 0xFF).to_bytes(1, byteOrder))


for idServo in range(1, 19):
    enableTorque(idServo)

print("torque enabled")

writePos(3, 0.6, 1)
time.sleep(2)
writePos(3, 0.8, 1)
time.sleep(2)
