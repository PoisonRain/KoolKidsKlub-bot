from elf_kingdom import *
from newMath import *
import Elf

locs = []

class Start:
    """ make a starting frame for the game, build starter portals, fountains etc 
    for normal to maintain"""
    def get_structure_ring_locations(self, game, elf, radius_from_castle, amount, structure_type = 0):
        """ builds a semi-ring of a structure (0 - portal, 1 - fountain) in a certain
        radius from our castle to the enemy castle"""
        start_location = game.get_my_castle().location
        end_location = start_location.towards(game.get_enemy_castle().location, radius_from_castle)
        
        target_points = [end_location] #list of locations to build portals in
        
        strt_alpha = get_alpha_from_points(start_location, end_location)
        pos_alpha = strt_alpha+5
        neg_alpha = strt_alpha-5
        
        while len(target_points) < amount and pos_alpha < strt_alpha+360 and neg_alpha > strt_alpha-360:
               
                pos_point = get_point_by_alpha(pos_alpha % 360, start_location, end_location)
                if self.can_build_portals_by_list(game, pos_point, target_points):
                    target_points.append(pos_point)
                    print 'pos_point: '+str(pos_point)
                    if len(target_points) >= amount:
                        break
                    
                pos_alpha += 5
                neg_point = get_point_by_alpha(neg_alpha % 360, start_location, end_location)
                if self.can_build_portals_by_list(game, neg_point, target_points):
                    target_points.append(neg_point)
                    print 'neg_point: '+str(neg_point)
                    if len(target_points) >= amount:
                        break
                    
                neg_alpha -= 5
                
        print target_points  
        return target_points
    
    def can_build_portal_at_updated(self, game, portal_location):
        return game.can_build_portal_at(portal_location) #and 0 < portal_location.col < game.cols and 0 < portal_location < game.rows
        
    def can_build_portals_by_list(self, game, portal_location, future_portals_list):
        """ tests whether a portal can be places in a location, after the portals in a
        list are built"""
        if not self.can_build_portal_at_updated(game, portal_location):
            return False
        for other_location in future_portals_list:
            if portal_location.in_range(other_location, game.portal_size*2):# 100 is a random number to prevent them from being stuck together
                return False
        return True
        
    
    def build_structure_ring(self, locs, elfDict):
        elfDict = dict(elfDict)
        for loc in locs:
            worker_elf = Elf.Elf.get_closest_elf(loc, elfDict)
            did_build = worker_elf.build_portal(loc)
            elfDict.pop(worker_elf, None)
            if did_build:
                locs.remove(loc)
        return locs
                

""" add the following code to do_turn for testing """
#  strtI = newStart.Start()
#     global defense_portal_locs
#     if game.turn == 1:
#         defense_portal_locs = strtI.get_structure_ring_locations(game, elfDict[my_elves[0].unique_id], 1000, 4)
    
#     if defense_portal_locs != []:
#         strtI.build_structure_ring(defense_portal_locs, elfDict)
