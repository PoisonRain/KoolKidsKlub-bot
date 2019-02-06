from elf_kingdom import *

global distance_from_line
distance_from_line = 500
global index, circ
index = -1
circ = list()

def start(game, elfDict):
    global index, circ
    my_castle_loc = game.get_my_castle().location
    enemy_castle_loc = game.get_enemy_castle().location
    m = -1/(float(my_castle_loc.row - enemy_castle_loc.row)/(enemy_castle_loc.col - my_castle_loc.col)) # the y axis is inverted, while the x is normal, and so is the slope formula
    b = my_castle_loc.row + m * my_castle_loc.col
    obstacle = game.get_my_living_elves()[0]
    elf = game.get_my_living_elves()[1]
    dis_from_obs = elf.distance(obstacle)
    if index < 0:
        circ = circle(dis_from_obs)
        for point in circ:
            point[1] += obstacle.location.col
            point[0] += obstacle.location.row
        max = 10
        first_point = None
        closest_points = [p for p in circ if abs(p[0] - elf.location.row) <=2]
        for p in closest_points:
            if abs(p[1] - elf.location.col) < max:
                max = abs(p[1] - elf.location.col)
                first_point = p
        index = circ.index(first_point)
    curr_point, index = next_point(circ, index, elf.max_speed)
    pos = Location(circ[index][0], circ[index][1])
    print(pos)
    elf.move_to(pos)


def circle(radius):
    "Bresenham complete circle algorithm in Python"
    # init vars
    switch = 3 - (2 * radius)
    points = [list() for x in xrange(8)]
    x = 0
    y = radius
    # first quarter/octant starts clockwise at 12 o'clock
    while x <= y:
        # first quarter first octant
        points[0].append([-y, x])
        # first quarter 2nd octant
        points[1].append([-x, y])
        # second quarter 3rd octant
        points[2].append([x, y])
        # second quarter 4.octant
        points[3].append([y, x])
        # third quarter 5.octant
        points[4].append([y, -x])        
        # third quarter 6.octant
        points[5].append([x, -y])
        # fourth quarter 7.octant
        points[6].append([-x, -y])
        # fourth quarter 8.octant
        points[7].append([-y, -x])
        if switch < 0:
            switch = switch + (4 * x) + 6
        else:
            switch = switch + (4 * (x - y)) + 10
            y = y - 1
        x = x + 1
    
    merged_points = []
    for p in points:
        merged_points += p

    return merged_points
    
def next_point(points, index, max_speed):
    index += 50
    if index == len(points):
        index = index - len(points)
    """curr_point = points[index]
    squared_dis = squared_distance(curr_point, points[index]) 
    while abs(squared_dis - (max_speed*max_speed)) >= 100:
        index += 1 
        if index == len(circ):
                index = 0
        squared_dis = squared_distance(curr_point, points[index])"""
    return points[index], index
    
def squared_distance(p1, p2):
    return (p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1]-p2[1]) * (p1[1]-p2[1])