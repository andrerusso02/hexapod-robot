
def print_coords(leg_list):
    for leg in leg_list:
        print("leg", leg.name, ":", leg.x, "    ", leg.y, "    ", leg.z, "    ", leg.put_down)
    print("")


def to_milis(delay_sec):
    return int(delay_sec * 1000)


def mapf(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def sign(x):
    return (x > 0) - (x < 0)