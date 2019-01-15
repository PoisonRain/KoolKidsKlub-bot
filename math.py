#check save

from elf_kingdom import *
import math

distance_to_avoid = 300  # magic num bluhhhhhh bad nu nu


def get_circle(start_point, mid_point,
               end_point):  # receive: three points return: radius and center point of the circle that passes through them

    x1 = start_point[0]

    x2 = mid_point[0]

    x3 = end_point[0]

    y1 = start_point[1]

    y2 = mid_point[1]

    y3 = end_point[1]

    incline_points12 = (y2 - y1) / (x2 - x1)

    incline_points23 = (y3 - y2) / (x3 - x2)

    if (incline_points12 == incline_points23):
        print 'not a circle ya dumbass'

    x = (incline_points12 * incline_points23 * (y3 - y1) + incline_points12 * (x2 + x3) - incline_points23 * (
    x1 + x2)) / (2 * (incline_points12 - incline_points23))

    y = (y1 + y2) / 2 - (x - (x1 + x2) / 2) / incline_points12

    radius = pow((pow((x2 - x), 2) + pow((y2 - y), 2)), 0.5)

    center = (x, y)

    return radius, center


def get_obstacle_distance_from_path(start_location, end_location,
                                    obstacle_location):  # recieve: start end and mid location return: distance of mid location from the path between the other two
    start_x = start_location[1]
    start_y = start_location[0]

    end_x = end_location[1]
    end_y = end_location[0]

    # get a line formula in the Ax+By+C=0 format

    A = (start_y - end_y)
    B = (end_x - start_x)
    C = (start_x * end_y - end_x * start_y)

    obstacle_x = obstacle_location[1]
    obstacle_y = obstacle_location[0]

    distance_from_path = abs((A * obstacle_x + B * obstacle_y + C) / math.sqrt(A * A + B * B))

    return abs(distance_from_path)


def get_side_for_maneuver(start_location, end_location,
                          obstacle_location):  # gets locations, return third point for maneuver
    start_x = start_location[0]
    start_y = start_location[1]

    end_x = end_location[0]
    end_y = end_location[1]
    
    distance_from_obstacle = 800

    if abs(start_x - end_x) > abs(start_y - end_y):  # if the y axis is the shorter one, move through that axis
        # get distance when lowering y, get distance when upping y
        new_midpoint_location_plus = (obstacle_location[0], obstacle_location[1] + distance_from_obstacle)
        new_midpoint_location_minus = (obstacle_location[0], obstacle_location[1] - distance_from_obstacle)
        distance_from_minus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_minus) #check which is the more efficent way
        distance_from_plus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_plus)

        if distance_from_minus > distance_from_plus: #take the best route
            return new_midpoint_location_plus
        else:
            return new_midpoint_location_minus

    else: #same thing, using x instead of y
        new_midpoint_location_plus = (obstacle_location[0] + distance_from_obstacle, obstacle_location[1])
        new_midpoint_location_minus = (obstacle_location[0] - distance_from_obstacle, obstacle_location[1])
        distance_from_minus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_minus)
        distance_from_plus = get_obstacle_distance_from_path(start_location, end_location, new_midpoint_location_plus)

        if distance_from_minus > distance_from_plus:
            return new_midpoint_location_plus
        else:
            return new_midpoint_location_minus


def get_next_point(circle_location, prev_a, distance_to_move, radius_from_obstacle): #gets the circle center, previous degree of shift, distance of string on circle and radius of avoiding, returns the next point and the new shift degree
#a,b = radius
#c = length to move
    prev_a = math.radians(prev_a) #turn from input degrees to radians for calc
    a = math.acos((radius_from_obstacle ** 2 + radius_from_obstacle ** 2 - distance_to_move ** 2)/( 2 * radius_from_obstacle * radius_from_obstacle)) #cosine rule to get degree of shift, get the radians from x positive
    a = a+prev_a
    print math.degrees(a)
    x = int(round(circle_location[1] + radius_from_obstacle * math.cos(a)))
    y = int(round(circle_location[0] + radius_from_obstacle * math.sin(a)))
    return (x,y) , math.degrees(a)


def get_degrees_from_point(point, circle_radius, circle_location):
    a = math.acos((point[1] - circle_location[1])/circle_radius)
    return math.degrees(a)

elf_in_target = False

def do_turn(game):
    if False:
        pass
    else:
        end_point = (game.get_enemy_castle().location.row, game.get_enemy_castle().location.col)
        start_point = (game.get_my_castle().location.row, game.get_my_castle().location.col)
        elf_location = (game.get_my_living_elves()[0].location.row, game.get_my_living_elves()[0].location.col)
        go_around = (1500,3700)
        
        print end_point
        print start_point
        
        mid_point = get_side_for_maneuver(start_point, end_point, go_around)
        print mid_point
        #radius, center = get_circle(end_point, mid_point, elf_location)
        
        #alpha = get_degrees_from_point(elf_location, radius, center)
        #next_point = get_next_point(center, alpha, 200, radius)[0]
        
        print 'elf going to:'
        global elf_in_target
        go_around_location = Location(go_around[0], go_around[1])
        if game.get_my_living_elves()[1].location != go_around_location:
            game.get_my_living_elves()[1].move_to(go_around_location)
        else:
            if get_obstacle_distance_from_path(start_point, end_point, go_around) < 800 and not elf_in_target:
                print get_obstacle_distance_from_path(start_point, end_point, go_around) 
                if elf_location==mid_point:
                    elf_in_target = True
                next_point = mid_point
            else:
                next_point = end_point
            
            next_point = Location(next_point[0], next_point[1])
            
            print next_point
            game.get_my_living_elves()[0].move_to(next_point)
        
        
 
