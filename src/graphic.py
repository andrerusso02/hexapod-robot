import matplotlib.pyplot as plt
import numpy as np


x_list = [0,0,0,0,0,0]
y_list = [0,0,0,0,0,0]
x_c_list = [0,0,0,0,0,0]
y_c_list = [0,0,0,0,0,0]
put_down = [0,0,0,0,0,0]

plt.ion()


def print_point(leg):
    global x_list, y_list, put_down
    # init
    plt.clf()
    plt.axis([-30, 30, -30, 30])
    # points du corps
    plt.plot([-3.5, -3.5, -3.5, 3.5, 3.5, 3.5], [7, 0, -7, 7, 0, -7], 'bs')
    # stocker toutes les coordonnées
    x_list[leg.name] = leg.x
    y_list[leg.name] = leg.y
    x_c_list[leg.name] = leg.x_center_area
    y_c_list[leg.name] = leg.y_center_area
    put_down[leg.name] = leg.put_down
    # points des pattes et cercles
    for i in range(0, 6):
        create_circle(x_c_list[i], y_c_list[i], leg.area_radius)
        if put_down[i]:
            plt.plot([x_list[i]], [y_list[i]], 'ko')
        else:
            plt.plot([x_list[i]], [y_list[i]], 'co')
    plt.draw()
    plt.pause(0.0001)



def create_circle(x, y, r):
    theta = np.linspace(0, 2*np.pi, 100)
    x1 = r * np.cos(theta) + x
    x2 = r * np.sin(theta) + y
    plt.plot(x1, x2, 'r')
