from math import *
from legs_moves import *
from util import *
import SCServo
import graphic
import sensors

class c_leg:

    def __init__(self, name, x_center_area, y_center_area, x_offset, y_offset, z_offset, ids_list, pin_button):
        self.name = name
        self.x_center_area = x_center_area
        self.y_center_area = y_center_area
        self.area_radius = 4
        self.x = x_center_area
        self.y = y_center_area
        self.z = 0
        self.x_current = x_center_area
        self.y_current = y_center_area
        self.z_current = 0
        self.ids_list = ids_list
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.put_down = False
        self.button = sensors.push_button(pin_button)
        SCServo.enableTorque(ids_list[0])
        SCServo.enableTorque(ids_list[1])
        SCServo.enableTorque(ids_list[2])

    """fl = from leg"""

    def get_x_fl(self):
        return self.x - self.x_offset

    def get_y_fl(self):
        return self.y - self.y_offset

    def get_z_fl(self):
        return self.z - self.z_offset

    def ground_detected(self):
        return self.button.pushed()

    def inside_area(self):
        # +0.1 : tolérance pour éviter les problèmes liés aux légères incertitudes lors des calucls
        return (self.x - self.x_center_area) ** 2 + (self.y - self.y_center_area) ** 2 <= self.area_radius ** 2 + 0.1

    def back_to_current_pos(self):
        self.x = self.x_current
        self.y = self.y_current
        self.z = self.z_current

    def angle_of_center(self):
        # angle entre l'axe y et le centre de la zone en passant par l'origine du repère
        # <---- +   - ----->
        d = sqrt(self.x_center_area**2 + self.y_center_area**2)
        angle_deg = degrees(-asin(self.x_center_area/d))
        if self.y_center_area < 0:
            angle_deg = 180 - angle_deg
        return angle_deg

    def set_pos(self, delay_sec, sim=False):
        if not sim:
            self.x_current = self.x
            self.y_current = self.y
            self.z_current = self.z

            l1 = 5.3
            l2 = 12.5
            l3 = 18.1
            x = self.get_x_fl()
            y = self.get_y_fl()
            z = self.get_z_fl()

            l = sqrt(x ** 2 + y ** 2)
            beta = sqrt(z ** 2 + (l - l1) ** 2)
            a = acos(y / l)
            b = acos((l3 ** 2 - l2 ** 2 - beta ** 2) / (-2 * l2 * sqrt(z ** 2 + (l - l1) ** 2))) + asin((l - l1) / beta)
            c = acos((z ** 2 + (l - l1) ** 2 - l2 ** 2 - l3 ** 2) / (-2 * l2 * l3))
            SCServo.writePos(self.ids_list[0], a, delay_sec)
            SCServo.writePos(self.ids_list[1], b, delay_sec)
            SCServo.writePos(self.ids_list[2], c, delay_sec)

            #graphic.print_point(self)
