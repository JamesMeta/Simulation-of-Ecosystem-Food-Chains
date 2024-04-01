# Code for generation of heightmaps for random resource distibution.
import random

screensize = [1920,1080]

def generate_resource_map(x_resolution, y_resolution):
    map = [[0 for y in range(y_resolution)] for x in range(x_resolution)]
    for x in range(x_resolution):
        for y in range(y_resolution):
            map[x][y] = random.randint(1,3)

    return map
