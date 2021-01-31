import SCServo
import time

moteurs = [3, 6]

for i in moteurs:
    SCServo.enableTorque(i)

t = 1

while True:
    for i in moteurs:
        SCServo.writePos(i, 0.5, t)
    time.sleep(t)
    for i in moteurs:
        SCServo.writePos(i, 1.5, t)
    time.sleep(t)
