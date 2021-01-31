import inputs
import time

"""
class ControllerInterface:
    def __init__(self):
        pass
"""

gamepad = inputs.devices.gamepads[0]

while 1:
    events = inputs.get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
