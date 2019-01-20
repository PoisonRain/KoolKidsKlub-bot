from elf_kingdom import *
import math

pi = math.pi

points = []
i = 0 #which point on the circle

def get_obstacle_distance_from_path(start_location, end_location,
                                    obstacle_location):  # recieve: start end and mid location return: distance of mid location from the path between the other two
    start_x = start_location[0]
    start_y = start_location[1]

    end_x = end_location[0]
    end_y = end_location[1]

    # get a line formula in the Ax+By+C=0 format

    A = (start_y - end_y)
    B = (end_x - start_x)
    C = (start_x * end_y - end_x * start_y)

    obstacle_x = obstacle_location[0]
    obstacle_y = obstacle_location[1]

    distance_from_path = abs((A * obstacle_x + B * obstacle_y + C) / math.sqrt(A * A + B * B))

    return abs(distance_from_path)


def get_side_for_maneuver(start_location, end_location,
                          obstacle_location, dist_to_go = 900):  # gets locations, return third point for maneuver
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

# def get_next_point(circle_location, prev_a, distance_to_move, radius_from_obstacle): #gets the circle center, previous degree of shift, distance of string on circle and radius of avoiding, returns the next point and the new shift degree
# #a,b = radius
# #c = length to move
#     prev_a = math.radians(prev_a) #turn from input degrees to radians for calc
#     a = math.acos((radius_from_obstacle ** 2 + radius_from_obstacle ** 2 - distance_to_move ** 2)/( 2 * radius_from_obstacle * radius_from_obstacle)) #cosine rule to get degree of shift, get the radians from x positive
#     a = a+prev_a
#     x = int(round(circle_location[0] + radius_from_obstacle * math.cos(a)))
#     y = int(round(circle_location[1] + radius_from_obstacle * math.sin(a)))
#     return (x,y) , math.degrees(a)

# def get_degrees_from_point(point, circle_radius, circle_location):
#     a = math.acos((point[0] - circle_location[0])/circle_radius)
#     return math.degrees(a)

def lineFromPoints(point1,point2):
    a = point2[0] - point1[0]
    b = point1[1] - point2[1]
    c = -(a * (point2[1]) + b * (point2[0]))

    return a,b,c

def normal_to_line_at_point(a,b,c, normal_point):#revieves line and a points and returns the perpendicular line at that point
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

def location_to_tuple(loc):
    return (loc.row,loc.col)
    
def tuple_to_location(tup):
    return Location(tup[0],tup[1])



def points_on_circle(axis_limits,center,r, string_distance = 100): #n needs to be generated with a function using the radius
 #this function needs to be used by finding the points closest to the wanted start and end locations, and running either forward
 #or backwards on the list, depending on which side is shorter that way upping efficency
    n = how_many_points_on_circle(r, string_distance) 
    return [(int(round(math.cos(2*pi/n*x)*r+center[0])),int(round(math.sin(2*pi/n*x)*r+center[1]))) 
    for x in range(0,n+1) if (axis_limits[0] > math.cos(2*pi/n*x)*r+center[0] > 0 
    and axis_limits[1] > math.sin(2*pi/n*x)*r+center[1] > 0)] ##list comprehenshion way, invalid syntax
    # ret_list = []
    # for x in range(0,n+1):
    #     row = math.cos(2*pi/n*x)*r+center[0]
    #     col = math.sin(2*pi/n*x)*r+center[1]
    #     if axis_limits[0] > row and row > 0 and axis_limits[1] > col and col > 0:
    #         ret_list.append((math.cos(2*pi/n*x)*r+center[0] , math.sin(2*pi/n*x)*r+center[1]))
    # return ret_list

def how_many_points_on_circle(radius, distance_to_move):
    alpha = math.acos((radius ** 2 + radius ** 2 - distance_to_move ** 2)/
    ( 2 * radius * radius)) #cosine rule to get degree of shift, get the radians from x positive
    return int(round(360/math.degrees(alpha)))
    

def closest_point_in_list(point, points_list):
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
    return (points_list.index(closest_point_in_list(start_point, points_list)), 
    points_list.index(closest_point_in_list(end_point,points_list)))
            
        

def manuver_move(game, elf, start_location, end_loc, manuver_loc, flank_distance):#recieves locations, objects and distances and performs the flanking
    
    global points
    global i
    
    manuver_to = get_side_for_maneuver(start_location, end_loc, manuver_loc, flank_distance)
    
    center, radius = get_circle(start_location, manuver_to, end_loc)
    if points == []:
        points = points_on_circle((game.rows, game.cols),center, radius)
    else:
        start_index, end_index = get_start_and_end_index(start_location, end_loc, points)
        next_tuple = points[i]
        if start_index < end_index: #changes wether you go forward or backwards
            if i == 0:
               i = start_index
               
            elif i < end_index:
                i+=1
            else:
                i = end_index
        else:
            if i == 0:
                i = start_index
            elif i > end_index:
                i-=1
            else:
                i = end_index
                
        next_point = Location(int(round(next_tuple[0])), int(round(next_tuple[1])))
        elf.move_to(next_point)
        print start_index
        print end_index
        print i

# manuver_back = False
# def do_turn(game):
#     global manuver_back
    
#     print manuver_back
#     enemy_castle = game.get_enemy_castle().location
#     enemy_castle_loc_test = (enemy_castle.row, enemy_castle.col) 
#     test_elf = game.get_my_living_elves()[0]
#     global manuver_back
    
#     if not manuver_back:
#         manuver_move(game, test_elf, (700,5800),(3100,700), (2200, 3000), 900)
        
#         if test_elf.location == Location(3096, 703):
#             manuver_back = True
       
#     if manuver_back:
#         manuver_move(game, test_elf, (3100,700), (700,5800), (2200, 3000), 900)
        
