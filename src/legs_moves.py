import time
from math import *
from util import *
from position_calculation import *


def legs_move_z(leg_list, delta):
    """Fait monter ou descendre toutes les pattes de delta."""
    step = 1
    delay = 0.1
    while abs(delta) >= step:
        for leg in leg_list:
            leg.z += sign(delta) * step
            leg.set_pos(delay)
        delta = sign(delta) * (abs(delta) - step)
        time.sleep(delay)
    if delta != 0:
        for leg in leg_list:
            leg.z += delta
            leg.set_pos(delay)
        time.sleep(delay)


def legs_put_down(leg_list, all_legs_list, ground_detection):
    """Ne donner que les pattes à poser. Rq : si une patte est déjà posée elle ne bougera pas"""
    if not ground_detection:
        delay = 0.5
        for leg in leg_list:
            leg.z = ground_highest_point(all_legs_list)
            leg.set_pos(delay)
            leg.put_down = True
        time.sleep(delay)
    else:
        step = 0.3
        delay = 0.05
        moved = True
        while moved:
            moved = False
            for leg in leg_list:
                if not leg.put_down:
                    if leg.ground_detected():
                        leg.put_down = True
                    else:
                        leg.z -= step
                        leg.set_pos(delay)
                        moved = True
            if moved:
                time.sleep(delay)


def legs_lift(leg_list, ground_detection):
    # Lève les pattes demandées
    heigh = 4
    delay = 0.5
    for leg in leg_list:
        if leg.put_down:
            if ground_detection:
                leg.z = 0
            else:
                leg.z += heigh
            leg.put_down = False
            leg.set_pos(delay)
    time.sleep(delay)



def legs_move_x_y(leg_list, distance, angle_deg, sim=False):
    """leg_list : la liste des pattes à déplacer; distance : la distance à parcourir;
    angle : en degrés, en augmentant l'angle les pattes vont vers la gauche"""
    delay = 0.1 * abs(distance)
    delta_x, delta_y = calc_deltas_for_move_x_y(distance, angle_deg)
    for leg in leg_list:
        leg.x += delta_x
        leg.y += delta_y
        leg.set_pos(delay, sim=sim)
    if not sim:
        time.sleep(delay)


def legs_go_to_area_border(leg_list, angle_deg):
    """déplace les pattes sélectionnées jusque sur le rayon de la zone autorisée, à l'angle indiqué.
    Attention ! cette fonction envoie l'ordre de positionnement mais n'attend pas !"""
    delay = 0.3
    for leg in leg_list:
        delta_x, delta_y = calc_deltas_for_move_x_y(leg.area_radius, angle_deg)
        leg.x = leg.x_center_area + delta_x
        leg.y = leg.y_center_area + delta_y
        leg.set_pos(delay)


def legs_rotate(axis, leg_list, angle_deg, sim=False):
    """angle_rad : la variation d'angle que l'on veut obtenir"""
    angle_rad = radians(angle_deg)
    delay = abs(angle_rad)
    for leg in leg_list:
        # quel axe ?
        if axis == 'x':
            absc, ord = leg.y, leg.z
        elif axis == 'y':
            absc, ord = leg.x, leg.z
        elif axis == 'z':
            absc, ord = leg.x, leg.y
        # calcul
        if absc != 0:
            current_a = atan(ord / absc)  # l'angle entre l'origine du repère et le bout de la patte
            dist = absc / cos(current_a)  # dist = la distance entre l'origine du repère et le bout de la patte
        elif ord > 0:
            current_a = pi/2
            dist = ord / sin(current_a)
        else:
            current_a = -pi/2
            dist = ord / sin(current_a)
        # current_a + angle_rad = l'angle cible, n_... : new
        n_abs = cos(current_a + angle_rad) * dist
        n_ord = sin(current_a + angle_rad) * dist
        if axis == 'x':
            leg.y, leg.z = n_abs, n_ord
        elif axis == 'y':
            leg.x, leg.z = n_abs, n_ord
        elif axis == 'z':
            leg.x, leg.y = n_abs, n_ord
        leg.set_pos(delay, sim=sim)
    if not sim:
        time.sleep(delay)