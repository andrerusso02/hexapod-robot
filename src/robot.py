from Leg import *
from legs_moves import *
from position_calculation import *
import sensors


height = 6

def init():
    leg_list = []
    leg_list.append(c_leg(0, -20, 14, -3.5, 7, 2.5, [1, 2, 3], 33))
    leg_list.append(c_leg(1, -21.5, -2, -3.5, 0, 2.5, [4, 5, 6], 35))
    leg_list.append(c_leg(2, -16, -20, -3.5, -7, 2.5, [7, 8, 9], 37))
    leg_list.append(c_leg(3, 20, 14, 3.5, 7, 2.5, [10, 11, 12], 36))
    leg_list.append(c_leg(4, 21.5, -2, 3.5, 0, 2.5, [13, 14, 15], 38))
    leg_list.append(c_leg(5, 16, -20, 3.5, -7, 2.5, [16, 17, 18], 40))
    time.sleep(0.1)
    return leg_list


def start(all_legs_list):
    global height
    for i in range(0, len(all_legs_list)):
        all_legs_list[i].set_pos(1)
    time.sleep(1)
    for i in range(0, len(all_legs_list)):
        all_legs_list[i].put_down = True
    legs_move_z(all_legs_list, -height)


def stop(all_legs_list, ground_detection):
    legs_put_down(all_legs_list, all_legs_list, ground_detection)


def shut_down(all_legs_list):
    # poser le corps au sol. Les pattes au dessus de z=1 s'arrètent de monte
    move = True
    while move:
        move = False
        legs_below_1_list = []
        for leg in all_legs_list:
            if leg.z < 1:
                legs_below_1_list.append(leg)
                move = True
        legs_move_z(legs_below_1_list, 1)
    # revenir à la position initiale
    delay = 1
    for leg in all_legs_list:
        leg.x = leg.x_center_area
        leg.y = leg.y_center_area
        leg.z = 0
        leg.set_pos(delay)
    time.sleep(delay)
    sensors.reset_gpio()


def walk_straight(all_legs_list, dir_angle_deg, ground_detection):
    """fait avancer d'un cm dans la direction donnée"""
    distance = -1  # à parcourir par les pattes, négative pour faire avancer le robot
    # l_legs_list : deux pattes à gauche, une à droite; r_legs_list : l'inverse.
    # side = l : deux pattes poées à gauche, une à droite : elles poussent le robot
    l_legs_list = [all_legs_list[0], all_legs_list[2], all_legs_list[4]]
    r_legs_list = [all_legs_list[1], all_legs_list[3], all_legs_list[5]]

    # initialisation :
    if are_put_down(l_legs_list) and are_up(r_legs_list):
        side = 'l'
        legs_down_list = l_legs_list
        legs_up_list = r_legs_list
    elif are_put_down(r_legs_list) and are_up(l_legs_list):
        side = 'r'
        legs_down_list = r_legs_list
        legs_up_list = l_legs_list
    else:
        # configuration pour créer le cas l.
        if not are_put_down(l_legs_list):
            legs_put_down(l_legs_list)
        legs_lift(r_legs_list, ground_detection)
        side = 'l'
        legs_down_list = l_legs_list
        legs_up_list = r_legs_list
    legs_go_to_area_border(legs_up_list, dir_angle_deg) #positionner correctement les pattes levées

    # tester si le mouvement est possible :
    legs_move_x_y(legs_down_list, distance, dir_angle_deg, sim=True)
    inside = inside_area(legs_down_list)
    for leg in legs_down_list:
        leg.back_to_current_pos()
    if not inside:
        print("repositionnement")
        # Passer d'un cas à l'autre (l à r ou inverse)
        # Poser les pattes levées, elles sont forcément à la bonne position.
        legs_put_down(legs_up_list, all_legs_list, ground_detection)
        # stabilisation si détection du sol activée
        if ground_detection:
            stabilize(all_legs_list)
        legs_lift(legs_down_list, ground_detection)
        if side == 'l':
            side = 'r'
            legs_down_list = r_legs_list
            legs_up_list = l_legs_list
        else:
            side = 'l'
            legs_down_list = l_legs_list
            legs_up_list = r_legs_list

    # déplacement
    legs_move_x_y(legs_down_list, distance, dir_angle_deg)



def turn(all_legs_list, direction, ground_detection):
    """fait tourner le robot de 3 degrés"""
    angle_deg = 3*sign(direction) # pour éviter d'avoir un angle différent de 3 ou moins 3
    l_legs_list = [all_legs_list[0], all_legs_list[2], all_legs_list[4]]
    r_legs_list = [all_legs_list[1], all_legs_list[3], all_legs_list[5]]

    # initialisation :
    if are_put_down(l_legs_list) and are_up(r_legs_list):
        side = 'l'
        legs_down_list = l_legs_list
        legs_up_list = r_legs_list
    elif are_put_down(r_legs_list) and are_up(l_legs_list):
        side = 'r'
        legs_down_list = r_legs_list
        legs_up_list = l_legs_list
    else:
        # configuration pour créer le cas l.
        if not are_put_down(l_legs_list):
            legs_put_down(l_legs_list)
        legs_lift(r_legs_list, ground_detection)
        side = 'l'
        legs_down_list = l_legs_list
        legs_up_list = r_legs_list
    # positionner correctement les pattes levées
    for leg in legs_up_list:
        start_angle = leg.angle_of_center() - sign(direction)*90
        legs_go_to_area_border([leg], start_angle)

    # tester si le mouvement est possible :
    legs_rotate('z', legs_down_list, angle_deg, sim=True)
    inside = inside_area(legs_down_list)
    for leg in legs_down_list:
        leg.back_to_current_pos()
    if not inside:
        print("repositionnement")
        # Passer d'un cas à l'autre (l à r ou inverse)
        # Poser les pattes levées, elles sont forcément à la bonne position.
        legs_put_down(legs_up_list, all_legs_list, ground_detection)
        # stabilisation si détection du sol activée
        if ground_detection:
            stabilize(all_legs_list)
        legs_lift(legs_down_list, ground_detection)
        if side == 'l':
            side = 'r'
            legs_down_list = r_legs_list
            legs_up_list = l_legs_list
        else:
            side = 'l'
            legs_down_list = l_legs_list
            legs_up_list = r_legs_list

    # rotation
    legs_rotate('z', legs_down_list, angle_deg)


def stabilize(leg_list):
    """donner les pattes posées"""

    # simuler la remise à l'applomb du sol
    move_angle_x = -angle_on_x_axis(leg_list)
    move_angle_y = -angle_on_y_axis(leg_list)
    legs_rotate('x', leg_list, move_angle_x, sim=True)
    legs_rotate('y', leg_list, move_angle_y, sim=True)

    # atténuer le mouvement en x quand le robot monte sur un truc
    # pour éviter que le robot se retrouve trop incliné par rapport au sol après et tombe
    height_diff = height_max(leg_list) - height_min(leg_list)
    if height_diff >= 3:
        angle_to_remove = 5
        legs_rotate('x', leg_list, -sign(move_angle_x)*angle_to_remove, sim=True)

    # bouger (ça effectue aussi les mouvements précédents)
    global height
    delay = 0.2
    delta_z = -ground_highest_point(leg_list) - height
    for leg in leg_list:
        leg.z += delta_z
        leg.set_pos(delay)
    time.sleep(delay)


def demo(all_leg_list):
    legs_move_z(all_leg_list, -3)
    legs_rotate('x', all_leg_list, 15, sim=False)
    legs_rotate('x', all_leg_list, -30, sim=False)
    legs_rotate('x', all_leg_list, 15, sim=False)
    legs_rotate('y', all_leg_list, 15, sim=False)
    legs_rotate('y', all_leg_list, -30, sim=False)
    legs_rotate('y', all_leg_list, 15, sim=False)
    legs_rotate('z', all_leg_list, 15, sim=False)
    legs_rotate('z', all_leg_list, -30, sim=False)
    legs_rotate('z', all_leg_list, 15, sim=False)
    legs_move_z(all_leg_list, 3)