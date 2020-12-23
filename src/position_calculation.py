from math import *


def ground_highest_point(leg_list):
    """donne la distance entre l'origine du robot et le point le plus haut du sol
    (negative du coup parce que c'est sous le robot)"""
    """impossible"""
    highest_point = -50
    for leg in leg_list:
        if leg.put_down and leg.z > highest_point:
            highest_point = leg.z
    return highest_point


def ground_lowest_point(leg_list):
    """donne la distance entre l'origine du robot et le point le plus bas du sol
    (negative du coup parce que c'est sous le robot)"""
    """impossible"""
    lowest_point = 50
    for leg in leg_list:
        if leg.put_down and leg.z < lowest_point:
            lowest_point = leg.z
    return lowest_point

def are_put_down(leg_list):
    all_put_down = True
    i = 0
    while all_put_down and i<len(leg_list):
        all_put_down = leg_list[i].put_down
        i+=1
    return all_put_down


def are_up(leg_list):
    all_up = True
    i = 0
    while all_up and i<len(leg_list):
        all_up = not leg_list[i].put_down
        i+=1
    return all_up


def angle_on_x_axis(leg_list):
    y_sum=0
    z_sum=0
    yz_sum=0
    square_y_sum=0
    for leg in leg_list:
        y_sum += leg.y
        z_sum += leg.z
        yz_sum += leg.y*leg.z
        square_y_sum += leg.y**2
    slope = (yz_sum/len(leg_list) - (y_sum/len(leg_list))*(z_sum/len(leg_list))) \
            / (square_y_sum/len(leg_list) + (y_sum/len(leg_list)**2))
    return degrees(atan(slope))


def angle_on_y_axis(leg_list):
    x_sum=0
    z_sum=0
    xz_sum=0
    square_x_sum=0
    for leg in leg_list:
        x_sum += leg.x
        z_sum += leg.z
        xz_sum += leg.x*leg.z
        square_x_sum += leg.x**2
    slope = (xz_sum/len(leg_list) - (x_sum/len(leg_list))*(z_sum/len(leg_list))) \
            / (square_x_sum/len(leg_list) + (x_sum/len(leg_list)**2))
    return degrees(atan(slope))


def calc_deltas_for_move_x_y(distance, angle_deg):
    """distance : la distance à parcourir; angle_deg : en augmentant l'angle
    les pattes vont vers la gauche, angle_deg=0 => pattes vers l'avant"""
    angle_rad = radians(angle_deg) +pi/2
    delta_x = cos(angle_rad)*distance
    delta_y = sin(angle_rad)*distance
    return delta_x, delta_y



def inside_area(leg_list):
    # False si au moins une patte est à l'extérieur de la zone.
    inside = True
    i = 0
    while inside and i<len(leg_list):
        inside = leg_list[i].inside_area()
        i += 1
    return inside


def height_max(leg_list):
    """donne le z de la patte la plus haute"""
    maxx = -50
    for leg in leg_list:
        if leg.z > maxx:
            maxx = leg.z
    return maxx


def height_min(leg_list):
    """donne le z de la patte la plus haute"""
    minn = 50
    for leg in leg_list:
        if leg.z < minn:
            minn = leg.z
    return minn


"""
def legs_down(legs_list):
    #renvoie les pattes posées parmi celles selectionnées
    legs_down_list = []
    for leg in legs_list:
        if leg.put_down:
            legs_down_list.append(leg)
    return legs_down_list
"""