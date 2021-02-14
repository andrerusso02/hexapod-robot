import inputs
import math
import robot
from threading import Thread


class ControllerInterface:

    def __init__(self):

        self.all_legs_list = robot.init()
        self.robotStandingUp = False

    def start(self):

        event_reader = ControllerEventReader()
        event_reader.start()

        while 1:
            if event_reader.last_event is not None:
                if event_reader.last_event.ev_type == "Key" and event_reader.last_event.code == "BTN_NORTH" and event_reader.last_event.state == 1:
                    if not self.robotStandingUp:
                        print("levé")
                        robot.start(self.all_legs_list)
                        self.robotStandingUp = True
                    else:
                        print("posé")
                        robot.stop(self.all_legs_list, False)
                        robot.shut_down(self.all_legs_list)
                        self.robotStandingUp = False

                elif event_reader.last_event.ev_type == "Key"\
                        and event_reader.last_event.code == "BTN_WEST"\
                        and event_reader.last_event.state == 1:
                    if self.robotStandingUp:
                        print("demo")
                        robot.demo(self.all_legs_list)

                elif event_reader.last_event.ev_type == "Absolute"\
                        and event_reader.last_event.code == "ABS_X"\
                        and self.robotStandingUp\
                        and event_reader.last_event.state != 0:
                    print("tourner")
                    robot.turn(self.all_legs_list, event_reader.last_event.state, False)

                elif self.robotStandingUp and event_reader.get_r_stick_angle() is not None:
                    robot.walk_straight(self.all_legs_list, 270 - event_reader.get_r_stick_angle(), False)

                elif not robot.are_all_legs_put_down(self.all_legs_list):
                    robot.legs_put_down(self.all_legs_list, self.all_legs_list, False)


class ControllerEventReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.last_event = None
        self.x_r_stick = 0
        self.y_r_stick = 0

    def run(self):
        while True:
            events = inputs.get_gamepad()
            for event in events:
                if event.ev_type != "Sync":
                    self.last_event = event
                if event.ev_type == "Absolute" and event.code == "ABS_RX":
                    if abs(event.state) > 10:
                        self.x_r_stick = event.state
                    else:
                        self.x_r_stick = 0
                elif event.ev_type == "Absolute" and event.code == "ABS_RY":
                    if abs(event.state) > 10:
                        self.y_r_stick = event.state
                    else:
                        self.y_r_stick = 0

    def get_r_stick_angle(self):
        if not (self.x_r_stick == 0.0 and self.y_r_stick == 0.0):
            return math.degrees(math.atan2(self.y_r_stick, self.x_r_stick))
        else:
            return None


if __name__ == '__main__':
    ControllerInterface().start()
