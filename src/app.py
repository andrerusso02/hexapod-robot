from tkinter import *
import robot
from threading import Thread


class c_robot_control(Thread):
    def __init__(self, all_legs_list):
        Thread.__init__(self)
        self.all_legs_list = all_legs_list
        self.angle = 0
        self.ground_detection = True
        self.straight = False
        self.right = False
        self.left = False
        self.shutdown = False
        self.demo = False

    def run(self):
        while True:
            if (self.straight):
                robot.walk_straight(self.all_legs_list, self.angle, ground_detection=self.ground_detection)
            if (self.left):
                robot.turn(all_legs_list, 1, ground_detection=self.ground_detection)
            if (self.right):
                robot.turn(all_legs_list, -1, ground_detection=self.ground_detection)
            if not self.straight and not self.left and not self.right:
               robot.stop(all_legs_list, ground_detection=self.ground_detection)
            if self.demo:
                robot.stop(self.all_legs_list, self.ground_detection)
                robot.demo(self.all_legs_list)
                self.demo = False
            """
            if self.shutdown:
                robotstop(all_legs_list, ground_detection=self.ground_detection)
                shut_down(all_legs_list)
            """

def set_straight():
    th_robot_control.left = False
    th_robot_control.right = False
    th_robot_control.straight = not th_robot_control.straight
    print("avancer :", th_robot_control.straight)


def set_left():
    th_robot_control.left = not th_robot_control.left
    th_robot_control.right = False
    th_robot_control.straight = False
    print("gauche :", th_robot_control.left)


def set_right():
    th_robot_control.left = False
    th_robot_control.right = not th_robot_control.right
    th_robot_control.straight = False
    print("droite :", th_robot_control.right)



def set_demo():
    th_robot_control.left = False
    th_robot_control.right = False
    th_robot_control.straight = False
    th_robot_control.demo = True
    print("demo")


"""  
def set_shut_down():
    th_robot_control.left = False
    th_robot_control.right = False
    th_robot_control.straight = False
    th_robot_control.shutdown = True
"""


def set_angle(angle):
    th_robot_control.angle = int(angle)


all_legs_list = robot.init()
robot.start(all_legs_list)

th_robot_control = c_robot_control(all_legs_list)
th_robot_control.start()

window = Tk()
ctrl_frm = Frame(window)
window.title("Robot Controller")
window.geometry("500x400")
start_btn = Button(window, text="straight", font=("Courrier, 20"), command=set_straight)
start_btn.pack(pady=20)
left_btn = Button(window, text="left", font=("Courrier, 20"), command=set_left)
left_btn.pack(pady=20)
right_btn = Button(window, text="right", font=("Courrier, 20"), command=set_right)
right_btn.pack(pady=20)
demo_btn = Button(window, text="demo", font=("Courrier, 20"), command=set_demo)
demo_btn.pack(pady=20)
"""
shtdn_btn = Button(window, text="shut down", font=("Courrier, 20"), command=set_shut_down)
shtdn_btn.pack(pady=20)
"""
angle_scale = Scale(ctrl_frm, orient='horizontal', from_=-180, to=180,
                    resolution=1, length=350, label="angle", command=set_angle)
angle_scale.pack()
ctrl_frm.pack(pady=30)
window.mainloop()