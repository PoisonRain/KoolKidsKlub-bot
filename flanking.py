from elf_kingdom import *
import math

pi = math.pi

POINTS = {}
I = {} #which point on the circle

def initialize(elfs):
    """
    initialize the global variables
    
    :list elfs: a list of all elfs in the game
    """
    global I
    global POINTS
    
    for elf in elfs:
        I[elf] = 0
        POINTS[elf] = []

"""
two functions that switch between the tuple representation and the tuple one
"""
def location_to_tuple(loc):
    return (loc.row,loc.col)
    
def tuple_to_location(tup):
    return Location(tup[0],tup[1])

def get_obstacle_distance_from_path(start_location, end_location,
                                    obstacle_location):  # recieve: start end and mid location return: distance of mid location from the path between the other two
    """
    draws a perpendicular line to the obstacle from the line between the end and
    start locations and returns that distance
    """
    start_x = start_location[0]
    start_y = start_location[1]

    end_x = end_location[0]
    end_y = end_location[1]

    # get a line formula in the Ax+By+C=0 format

    A = (start_y - end_y)
    B = (end_x - start_x)
    C = (start_x * end_y - end_x * start_y)
    
    # A,B,C = lineFromPoints(start_location, end_location) # doesnt work for some reason

    obstacle_x = obstacle_location[0]
    obstacle_y = obstacle_location[1]
    try:
        distance_from_path = abs((A * obstacle_x + B * obstacle_y + C) / math.sqrt(A * A + B * B))
    
        return distance_from_path
    except:
        return 0

def get_side_for_maneuver(start_location, end_location,
                          obstacle_location, dist_to_go = 900):  # gets locations, return third point for maneuver
    
    """
    finds out which distance is shorter, x or y, and adds to that the distance
    needed and returns the point to which the manuver should go
    
    :tuple start_location: the origin location for the manuver
    :tuple end_location: the target location
    :tuple obstacle_location: the location of the object to avoid
    :param dist_to_go: how much to add/subtract from the chosen axis away from obstacle
    """
    start_x = start_location[0]
    start_y = start_location[1]

    end_x = end_location[0]
    end_y = end_location[1]

    if abs(start_x - end_x) > abs(start_y - end_y):  # if the y axis is the shorter one, move through that axis
        # get distance when lowering y, get distance when upping y
        new_midpoint_location_plus = (obstacle_location[0], obstacle_location[1] + dist_to_go)
        new_midpoint_location_minus = (obstacle_location[0], obstacle_location[1] - dist_to_go)
        distance_from_minus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_minus) #check which is the more efficent way
        distance_from_plus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_plus)

        if distance_from_minus > distance_from_plus: #take the best route
            return new_midpoint_location_plus
        else:
            return new_midpoint_location_minus

    else: #same thing, using x instead of y
        new_midpoint_location_plus = (obstacle_location[0] + dist_to_go, obstacle_location[1])
        new_midpoint_location_minus = (obstacle_location[0] - dist_to_go, obstacle_location[1])
        distance_from_minus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_minus)
        distance_from_plus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_plus)

        if distance_from_minus > distance_from_plus:
            return new_midpoint_location_plus
        else:
            return new_midpoint_location_minus


def lineFromPoints(point1,point2): # needs to be checked out again
    """
    recieves two points(in tuple form) and returns the line that goes through 
    them in the form of: 'ay+bx+c = 0'
    """
    a = point2[0] - point1[0]
    b = point1[1] - point2[1]
    c = -(a * (point2[1]) + b * (point2[0]))

    return a,b,c

def normal_to_line_at_point(a,b,c, normal_point):#revieves line and a points and returns the perpendicular line at that point
    """
    recieves line in the form of: 'ay+bx+c = 0' and returns the perpendicular line
    to that line in the same form
    
    :tuple normal_point: the point where the normal to the line is drawn
    
    """
    if a == 0:
        new_a = 1
        new_b = 0
        new_c = normal_point[1]

        return new_a, new_b, new_c

    elif b == 0:
        new_a = 0
        new_b = 1
        new_c = normal_point[0]

        return new_a, new_b, new_c

    else:
        m = float(-b)/a
        m = (-1.0/m)
        new_a = 1
        new_b = -m
        new_c = -normal_point[1] + m * normal_point[0]
        return new_a, new_b, new_c

def clash_point_of_lines(a1,b1,c1,a2,b2,c2): #recieves two lines in normal form, returns clash point if exists or None if not
    """
    recieves two lines in the form of: 'ay+bx+c = 0' and returns the point where 
    they meet(tuple form)
    """
    if a1 == 0: #if the function is Bx = C
        if a2 == 0: #if both functions are in this form
            if c1/b1==c2/b2:#if the x is the same
                return ((-c1/b1),0) #returns 0 y by default, can be any y
            else:
                return None #no clash
        else:
            return ((-c1/b1),(-b2*(-c1/b1)-c2)/a2) #calculating the clash point (-B2*X1-C2)/A2
    elif a2 == 0:
        if a1 == 0: #if both functions are in this form
            if c2/b2==c1/b1:#if the x is the same
                return ((-c1/b1),0) #returns 0 y by default, can be any y
            else:
                return None #no clash
        else:
            return ((-c2/b2),(-b1*(-c2/b2)-c1)/a1) #calculating the clash point (-B1*X2-C1)/A1

    else:
        #turn functions into y=mx+b form for easier calc
        m1 = float(-b1)/a1
        b1 = float(-c1)/a1
        m2 = float(-b2) / a2
        b2 = float(-c2) / a2

        if m1 == m2:
            if b1 == b2:
                return (0, b1)
            else:
                return None
        else:
            return_x = (b2-b1)/(m1-m2)
            return_y = m1*return_x+b1
            return (return_x,return_y) #round needed, cause its the mid point or nah?

def get_circle(point1, point2, point3):
    """
    receives 3 points in tuple form and returns the center point(tuple) and
    radius of the circle that goes through them
    """
    A = point1
    B = point2
    C = point3
    a1, b1, c1 = lineFromPoints(A, B)  # works
    mid_point = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    a1, b1, c1 = normal_to_line_at_point(a1, b1, c1, mid_point)  # works

    a2, b2, c2 = lineFromPoints(A, C)  # works
    mid_point = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    a2, b2, c2 = normal_to_line_at_point(a2, b2, c2, mid_point)  # works
    center_point = clash_point_of_lines(a1, b1, c1, a2, b2, c2)
    
    
    circle_rad = math.sqrt(
        (A[0] - center_point[0]) ** 2 + (A[1] - center_point[1]) ** 2)  # check the rad using distance function
    return center_point, circle_rad


def points_on_circle(axis_limits,center,r, string_distance = 100): #100 is the default elf speed
    """
    returns all the points on a circle which are valid(inside the screen limits)
    
    :tuple axis_limits: the game.rows and game.cols
    :tuple center: the center point of the circles path
    :param r: the radius of the circles path
    :param string_distance: how far away should every two points be
    """
    n = how_many_points_on_circle(r, string_distance) 
    return [(int(round(math.cos(2*pi/n*x)*r+center[0])),int(round(math.sin(2*pi/n*x)*r+center[1]))) 
    for x in range(0,n+1) if (axis_limits[0] > math.cos(2*pi/n*x)*r+center[0] > 0 
    and axis_limits[1] > math.sin(2*pi/n*x)*r+center[1] > 0)] ##list comprehenshion way
    # ret_list = []
    # for x in range(0,n+1):
    #     row = math.cos(2*pi/n*x)*r+center[0]
    #     col = math.sin(2*pi/n*x)*r+center[1]
    #     if axis_limits[0] > row and row > 0 and axis_limits[1] > col and col > 0:
    #         ret_list.append((math.cos(2*pi/n*x)*r+center[0] , math.sin(2*pi/n*x)*r+center[1]))
    # return ret_list

def how_many_points_on_circle(radius, distance_to_move):
    """
    find how many points need to be generated on a circle to have a certain
    distance between every two points 
    """
    alpha = math.acos((radius ** 2 + radius ** 2 - distance_to_move ** 2)/
    ( 2 * radius * radius)) #cosine rule to get degree of shift, get the radians from x positive
    return int(round(360/math.degrees(alpha)))
    

def closest_point_in_list(point, points_list):
    """
    find the closest point in a list to a given point
    """
    point_location = tuple_to_location(point)
    min_distnace = point_location.distance(tuple_to_location(points_list[0]))
    min_point = points_list[0]
    
    for other in points_list:
        distance_to_other = point_location.distance(tuple_to_location(other))
        if  distance_to_other < min_distnace:
            min_distnace = distance_to_other
            min_point = other
            
    return min_point
    
def get_start_and_end_index(start_point, end_point, points_list):
    """
    returns the indexes in the list of points on circle path
    
    :param start_point: the starting location of the elf
    :param end_point: the target location
    :list points_list: the points generated on the circle path
    """
    return (points_list.index(closest_point_in_list(start_point, points_list)), 
    points_list.index(closest_point_in_list(end_point,points_list)))
            
def object_to_manuver(elf_loc, start_loc, end_loc, obstacle_location_list):
    """
    finds the closest obstacle that needs to be manuvered around
    
    :param elf_loc: the current elf location
    :param start_loc: the location the manuver started at(where the function was first called)
    :param end_loc: the target location 
    :list obstacle_locations: a list of all the locations of the obstacles to avoid(in tuple form)
    """
    obstacle_distance = 900
    for obstacle in obstacle_location_list:
        obstacles_in_way = [i for i in obstacle_location_list if get_obstacle_distance_from_path(start_loc, end_loc, i) < 900]
    
    if len(obstacles_in_way) == 0:
        return None
    return closest_point_in_list(elf_loc, obstacles_in_way)

def manuver_move(game, elf, start_location, end_loc, flank_distance, obstacle_locations):#recieves locations, objects and distances and performs the flanking
    """
    puts all the functions to use and actually sends commands to the elf
   
   :param elf: the elf moving
   :param start_location: the location the manuver started at(where the function was first called)
   :param end_loc: the target location 
   :param flank_distance: how far from the obstacle should the elf swerve
   :list obstacle_locations: a list of all the locations of the obstacles to avoid(in tuple form)
    """
    global POINTS
    global I
    
    elf_loc = location_to_tuple(elf.location)
    manuver_loc = object_to_manuver(elf_loc, start_location, end_loc, obstacle_locations)
    if manuver_loc is None:
        elf.move_to(tuple_to_location(end_loc))
        print 'moving to '+str(end_loc)
    else:
        manuver_to = get_side_for_maneuver(start_location, end_loc, manuver_loc, flank_distance)
        
        center, radius = get_circle(start_location, manuver_to, end_loc)
        POINTS[elf] = points_on_circle((game.rows, game.cols),center, radius)
        
        start_index, end_index = get_start_and_end_index(start_location, end_loc, POINTS[elf])
        next_tuple = POINTS[elf][I[elf]]
        if start_index < end_index: #changes wether you go forward or backwards
            if I[elf] == 0:
               I[elf] = start_index
               
            elif I[elf] < end_index: #elif may need to be changed to if
                I[elf]+=1
            else:
                I[elf] = end_index
        else:
            if I[elf] == 0:
                I[elf] = start_index
            elif I[elf] > end_index:
                I[elf]-=1
            else:
                I[elf] = end_index
                    
        next_point = Location(int(round(next_tuple[0])), int(round(next_tuple[1])))
        print start_index
        print end_index
        print I[elf]
        print next_point
        elf.move_to(next_point)
        
        


#veryyyyyyyyyy trash test code:

# import flanking

# def do_turn(game):
#     elves = game.get_all_my_elves()
#     if game.turn == 1:
#         flanking.initialize(elves)
#     else:
#         flanking.manuver_move(game, elves[0], (3040, 620), (600, 5600), 2000, [(2020, 2890)])
#         flanking.manuver_move(game, elves[1], (3040, 620), (3450, 3550), 2000, [(2020, 2890)])