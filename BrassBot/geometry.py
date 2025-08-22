import random
from sc2.position import Point2
from .option import Option, chose_option
import math
import numpy
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.game_data import AbilityData
from .building_line_group import BuildingLineWidth


class Geometry():
    directions = [Point2([1,0]), Point2([1,1]), Point2([0,1]), Point2([-1,1]), Point2([-1,0]), Point2([-1,-1]), Point2([0,-1]), Point2([1,-1])]
    building_tech_lab_structure_layout = [Point2([-1,-1]),Point2([-1,0]),Point2([-1,1]),Point2([0,-1]),Point2([0,0]),Point2([0,1]),Point2([1,-1]),Point2([1,0]),Point2([1,1]),Point2([2,0]),Point2([2,-1]),Point2([3,0]),Point2([3,-1])]
    building_3x3 = [Point2([-1,-1]),Point2([-1,0]),Point2([-1,1]),Point2([0,-1]),Point2([0,0]),Point2([0,1]),Point2([1,-1]),Point2([1,0]),Point2([1,1])]
    building_2x2 = [Point2([0.5,0.5]),Point2([-0.5,0.5]),Point2([0.5,-0.5]),Point2([-0.5,-0.5])]
    addon_offset = Point2([2.5, -0.5])

    def __init__(self,bot):
        self.bot = bot

    def get_angle_from_point(self, point):
        length = point.distance_to(Point2([0,0]))
        return math.acos((math.pow(length, 2) + math.pow(point.x, 2) - math.pow(point.y, 2)) / ( 2 * length * point.x))
    
    def get_point_from_angle(self, angle):
        #print(numpy.rad2deg(angle))
        return Point2([math.sin(numpy.deg2rad(90) - angle), math.sin(angle)])

    def get_points_in_angle(self, point, angle):
        original_angle = None
        if point.x == 0:
            if point.y > 0:
                original_angle = 270
            elif point.y < 0:
                original_angle = 90
            else:
                original_angle = random.randint(0, 359)
        elif point.y == 0:
            if point.y > 0:
                original_angle = 0
            else:
                original_angle = 180
        else:
            original_angle = self.get_angle_from_point(point)
        #print(numpy.rad2deg(original_angle))
        return [self.get_point_from_angle(original_angle + angle), self.get_point_from_angle(original_angle - angle)]
    
    def get_random_direction(self):
        return self.directions[random.randint(0, len(self.directions) -1)]
    
    def get_threats(self, position, ground = True, extra_range = 0, exclude_workers = False):
        exclude_units = {UnitTypeId.CHANGELING}
        if exclude_workers:
            exclude_units = {UnitTypeId.CHANGELING, UnitTypeId.SCV, UnitTypeId.DRONE, UnitTypeId.PROBE, UnitTypeId.MULE}
        if ground:
            return self.bot.enemy_units.exclude_type(exclude_units).filter(lambda enemy: enemy.can_attack_ground and enemy.distance_to(position) <= enemy.ground_range + extra_range)
        else:
            return self.bot.enemy_units.exclude_type(exclude_units).filter(lambda enemy: enemy.can_attack_air and enemy.distance_to(position) <= enemy.air_range + extra_range)

    def get_nearby_enemy_structures(self, position, range, structure_filter, only_ready):
        return self.bot.enemy_structures.closer_than(range , position).filter(lambda unit: (structure_filter == None or unit.type_id in structure_filter) and (not only_ready or unit.is_ready))

    def get_center_of_units(self, units):
        if len(units) == 0:
            return Point2([0,0])
        sum = Point2([0,0])
        for unit in units:
            sum += unit.position
        return sum / len(units)
    
    def get_center_of_effects(self, effects):
        if len(effects) == 0:
            return Point2([0,0])
        sum = Point2([0,0])
        for effect in effects:
            sum += list(effect.positions)[0]
        return sum / len(effects)
    
    def get_center_of_abstract_units(self, units):
        if len(units) == 0:
            return Point2([0,0])
        sum = Point2([0,0])
        for unit in units:
            sum += unit.get_self().position
        return sum / len(units)
    
    def get_exit_route_options_1(self, start, ground = True):
        options = []
        for direction in self.directions:
            distance = 1
            if ground:
                while self.bot.in_pathing_grid(start + direction*distance):
                    distance += 1
            else:
                while self.bot.in_map_bounds(start + direction*distance):
                    distance += 1
            threats = []
            if ground:
                threats = self.bot.enemy_units.filter(lambda enemy: enemy.can_attack_ground and (enemy.distance_to(start.towards(start + direction, 4)) < max(5, enemy.ground_range) or enemy.distance_to(start.towards(start + direction, 8)) < max(5, enemy.ground_range) or enemy.distance_to(start.towards(start + direction, 12)) < max(5, enemy.ground_range)))
            else:
                threats = self.bot.enemy_units.filter(lambda enemy: enemy.can_attack_air and (enemy.distance_to(start.towards(start + direction, 4)) < max(5, enemy.air_range) or enemy.distance_to(start.towards(start + direction, 8)) < max(5, enemy.air_range) or enemy.distance_to(start.towards(start + direction, 12)) < max(5, enemy.air_range)))
            options.append(Option(self.bot, max(7 ,distance)- len(threats) * 5, direction))
        return options
    
    def get_exit_route_options_2(self, start, previous_flee_direction = None, ground = True):
        options = []
        threats = self.get_threats(start, ground, 5)
        if len(threats) > 0:
            center = self.get_center_of_units(threats)
            ideal_direction = start - center
            distance = 0
            if ground:
                while self.bot.in_pathing_grid(start.towards(ideal_direction, distance)):
                    distance += 1
            else:
                while self.bot.in_map_bounds(start.towards(ideal_direction, distance)):
                    distance += 1
            options.append(Option(self.bot, 1 + distance, ideal_direction))
            other_directions = self.get_points_in_angle(ideal_direction, numpy.deg2rad(45))
            #print(print(ideal_direction, other_directions))
            for direction in other_directions:
                distance = 0
                if ground:
                    while self.bot.in_pathing_grid(start.towards(direction, distance)):
                        distance += 1
                else:
                    while self.bot.in_map_bounds(start.towards(direction, distance)):
                        distance += 1
                options.append(Option(self.bot, 1 + distance/1.2, direction))
            other_directions = self.get_points_in_angle(ideal_direction, numpy.deg2rad(90))
            #print(print(ideal_direction, other_directions))
            for direction in other_directions:
                distance = 0
                if ground:
                    while self.bot.in_pathing_grid(start.towards(direction, distance)):
                        distance += 1
                else:
                    while self.bot.in_map_bounds(start.towards(direction, distance)):
                        distance += 1
                options.append(Option(self.bot, 1 + distance/1.6, direction))
        elif previous_flee_direction != None:
            options.append(Option(self.bot, 1, previous_flee_direction))
        else:
            options.append(Option(self.bot, 1, self.get_random_direction()))
        return options
    
    def get_best_exit_route(self, start, previous_flee_direction = None, ground = True):
        return chose_option(self.get_exit_route_options_2(start, previous_flee_direction, ground)).what
    
    def get_nearest_enemy(self, start, can_ground = True, can_air = True, only_revealed = False):
        units = []
        if only_revealed:
            units = self.bot.enemy_units.exclude_type(self.bot.static_instructions.ignored_targets).filter(lambda unit: (unit._proto.is_flying and can_air) or (not unit._proto.is_flying and can_ground) or unit.type_id == UnitTypeId.COLOSSUS and unit.can_be_attacked)
        else:
            units = self.bot.enemy_units.exclude_type(self.bot.static_instructions.ignored_targets).filter(lambda unit: (unit._proto.is_flying and can_air) or (not unit._proto.is_flying and can_ground) or unit.type_id == UnitTypeId.COLOSSUS)
        if len(units) > 0:
            return units.closest_to(start)
        
    def get_enemies_in_range(self, unit, can_ground, can_air, can_structure, bonus_range = 0, only_revealed = False):
        actual_unit = unit.get_self()
        units = self.bot.enemy_units.exclude_type(self.bot.static_instructions.ignored_targets).filter(lambda target: self.is_target_in_range(actual_unit, target, bonus_range) and
                                            (((can_air or not target._proto.is_flying) and
                                            (can_ground or target._proto.is_flying)) or target.type_id == UnitTypeId.COLOSSUS)
                                            and (target.can_be_attacked or not only_revealed))
        if can_structure:
            return units + self.bot.enemy_structures.exclude_type(self.bot.static_instructions.ignored_targets).filter(lambda target: self.is_target_in_range(actual_unit, target, bonus_range) and
                                            ((can_air or not target._proto.is_flying) and
                                            (can_ground or target._proto.is_flying))
                                            and (target.can_be_attacked or not only_revealed))
        return units
    
    def is_target_in_range(self, actual_unit, target, bonus_range = 0) -> bool:
        try:
            if actual_unit.can_attack_ground and not target.is_flying:
                unit_attack_range = actual_unit.ground_range
            elif actual_unit.can_attack_air and (target.is_flying or target.type_id == UnitTypeId.COLOSSUS):
                unit_attack_range = actual_unit.air_range
            else:
                return False
            return actual_unit.position.distance_to(target.position) <= actual_unit.radius + target.radius + unit_attack_range + bonus_range
        except:
            self.bot.chat.add_to_chat_queue("That range error again.")
        return False
        
    def get_nearest_enemy_structure(self, start, can_ground = True, can_air = True):
        units = self.bot.enemy_structures.filter(lambda unit: (unit._proto.is_flying and can_air) or (not unit._proto.is_flying and can_ground))
        if len(units) > 0:
            return units.closest_to(start)
        
    def get_random_spot(self):
        random_x = random.randrange(self.bot._game_info.playable_area.x, self.bot._game_info.playable_area.x + self.bot.game_info.playable_area.width)
        random_y = random.randrange(self.bot._game_info.playable_area.y, self.bot._game_info.playable_area.y + self.bot.game_info.playable_area.height)
        return Point2([random_x, random_y])
    
    async def can_place_2x2_fast(self, point):
        for building_square in self.building_2x2:
            current_point = point + building_square
            if not self.bot.in_map_bounds(current_point) or not self.bot.in_placement_grid(current_point):
                # print(self.bot.iteration, False, point + building_square)
                return False
        # print(self.bot.iteration, True, point)
        return True
    
    async def can_place_3x3_fast(self, point):
        for building_square in self.building_3x3:
            current_point = point + building_square
            if not self.bot.in_map_bounds(current_point) or not self.bot.in_placement_grid(current_point):
                # print(self.bot.iteration, False, point + building_square)
                return False
        # print(self.bot.iteration, True, point)
        return True
    
    async def can_place_building_tech_lab_fast(self, point):
        for building_square in self.building_tech_lab_structure_layout:
            current_point = point + building_square
            if not self.bot.in_map_bounds(current_point) or not self.bot.in_placement_grid(current_point):
                # print(self.bot.iteration, False, point + building_square)
                return False
        # print(self.bot.iteration, True, point)
        return True

    async def can_place_2x2(self, point):
        if await self.bot.can_place_single(AbilityId.TERRANBUILD_SUPPLYDEPOT, point):
            return True
        return False

    async def can_place_3x3(self, point):
        if await self.bot.can_place_single(AbilityId.TERRANBUILD_ENGINEERINGBAY, point):
            return True
        return False
    
    async def can_place_building_tech_lab(self, point):
        if (await self.bot.can_place_single(AbilityId.TERRANBUILD_ENGINEERINGBAY, point)) and (await self.bot.can_place_single(AbilityId.TERRANBUILD_SUPPLYDEPOT, point + self.addon_offset)):
            return True
        return False
    
    async def is_with_addon_in_building_line_grid(self, point):
        from .building_line_group import BuildingLineGroup
        for group in self.bot.root_groups:
            if type(group) == BuildingLineGroup:
                for point_offset in self.building_tech_lab_structure_layout:
                    point_offseted = point + point_offset
                    if point_offseted.x >= group.left_x and point_offseted.x <= group.left_x + group.get_with_lenght() and point_offseted.y >= group.bottom_y and point_offseted.y <= group.top_y:
                        return True
        return False
    
    async def is_3x3_in_building_line_grid(self, point):
        from .building_line_group import BuildingLineGroup
        for group in self.bot.root_groups:
            if type(group) == BuildingLineGroup:
                for point_offset in self.building_3x3:
                    point_offseted = point + point_offset
                    if point_offseted.x >= group.left_x and point_offseted.x <= group.left_x + group.get_with_lenght() and point_offseted.y >= group.bottom_y and point_offseted.y <= group.top_y:
                        return True
        return False
    
    async def is_2x2_in_building_line_grid(self, point):
        from .building_line_group import BuildingLineGroup
        for group in self.bot.root_groups:
            if type(group) == BuildingLineGroup:
                for point_offset in self.building_2x2:
                    point_offseted = point + point_offset
                    #print("offseted =",point_offseted)
                    if point_offseted.x >= group.left_x and point_offseted.x <= group.left_x + group.get_with_lenght() and point_offseted.y >= group.bottom_y and point_offseted.y <= group.top_y:
                        return True
        return False
    
    async def get_parameters_for_building_line_group_near(self, around, radius = 9, width = BuildingLineWidth.WITHADDONS):
        #print(radius, width)
        options = []
        for y_center in range(int(around.y) - radius, int(around.y) + radius, radius):
            for x_center in range(int(around.x) - radius -6, int(around.x) + radius +6, 1):
                center = Point2([x_center, y_center])
                #print("center =", center)
                if width == BuildingLineWidth.WITHADDONS:
                    if self.get_to_nearby_mineral_field(center, 6) != [] or not await self.can_place_building_tech_lab_fast(center) or await self.is_with_addon_in_building_line_grid(center):
                        continue
                    up_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center + Point2([0, up_space]), 4) == [] and await self.can_place_building_tech_lab_fast(center + Point2([0, up_space])) and not await self.is_with_addon_in_building_line_grid(center + Point2([0, up_space])):
                        up_space += self.get_line_step(width)
                    down_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center - Point2([0, down_space]), 4) == [] and await self.can_place_building_tech_lab_fast(center - Point2([0, down_space])) and not await self.is_with_addon_in_building_line_grid(center - Point2([0, up_space])):
                        down_space += self.get_line_step(width)
                    left_x = x_center - 1
                    top_y = y_center + up_space - 2 #tyhle konstanty jsou možná blbě
                    bottom_y = y_center - down_space + 2 #tyhle konstanty jsou možná blbě
                    from_top = Point2([left_x, bottom_y]).distance_to(around) > Point2([left_x, top_y]).distance_to(around)
                    is_same_height = self.bot.get_terrain_height(around) == self.bot.get_terrain_height(Point2([left_x, bottom_y]))
                    option = Option(self.bot, motivation= up_space+down_space if is_same_height else (up_space+down_space)/200, what=[left_x, top_y, bottom_y, from_top])
                    options.append(option)
                elif width == BuildingLineWidth.THREEWIDE:
                    if self.get_to_nearby_mineral_field(center, 4) != [] or not await self.can_place_3x3_fast(center) or await self.is_3x3_in_building_line_grid(center):
                        continue
                    up_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center + Point2([0, up_space]), 4) == [] and await self.can_place_3x3_fast(center + Point2([0, up_space])) and not await self.is_3x3_in_building_line_grid(center + Point2([0, up_space])):
                        up_space += self.get_line_step(width)
                    down_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center - Point2([0, down_space]), 4) == [] and await self.can_place_3x3_fast(center - Point2([0, down_space])) and not await self.is_3x3_in_building_line_grid(center - Point2([0, up_space])):
                        down_space += self.get_line_step(width)
                    left_x = x_center - 1
                    top_y = y_center + up_space - 2 #tyhle konstanty jsou možná blbě
                    bottom_y = y_center - down_space + 2 #tyhle konstanty jsou možná blbě
                    from_top = Point2([left_x, bottom_y]).distance_to(around) > Point2([left_x, top_y]).distance_to(around)
                    is_same_height = self.bot.get_terrain_height(around) == self.bot.get_terrain_height(Point2([left_x, bottom_y]))
                    option = Option(self.bot, motivation= up_space+down_space if is_same_height else (up_space+down_space)/200, what=[left_x, top_y, bottom_y, from_top])
                    options.append(option)
                elif width == BuildingLineWidth.TWOWIDE:
                    center = Point2([x_center + 0.5, y_center + 0.5])
                    if self.get_to_nearby_mineral_field(center, 4) != [] or not await self.can_place_2x2_fast(center) or await self.is_2x2_in_building_line_grid(center):
                        continue
                    up_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center + Point2([0, up_space]), 4) == [] and await self.can_place_2x2_fast(center + Point2([0, up_space])) and not await self.is_2x2_in_building_line_grid(center + Point2([0, up_space])):
                        up_space += self.get_line_step(width)
                    down_space = self.get_line_step(width)
                    while self.get_to_nearby_mineral_field(center - Point2([0, down_space]), 4) == [] and await self.can_place_2x2_fast(center - Point2([0, down_space])) and not await self.is_2x2_in_building_line_grid(center - Point2([0, up_space])):
                        down_space += self.get_line_step(width)
                    left_x = x_center - 0.5
                    top_y = y_center + up_space - 1 #tyhle konstanty jsou možná blbě
                    bottom_y = y_center - down_space + 2 #tyhle konstanty jsou možná blbě
                    from_top = Point2([left_x, bottom_y]).distance_to(around) > Point2([left_x, top_y]).distance_to(around)
                    is_same_height = self.bot.get_terrain_height(around) == self.bot.get_terrain_height(Point2([left_x, bottom_y]))
                    option = Option(self.bot, motivation= up_space+down_space if is_same_height else (up_space+down_space)/200, what=[left_x, top_y, bottom_y, from_top])
                    options.append(option)
        if len(options) == 0:
            return await self.get_parameters_for_building_line_group_near(around, int(radius*1.3))
        return chose_option(options).what
        
    def get_line_step(self, width):
        if width == BuildingLineWidth.TWOWIDE:
            return 2
        return 3
    
    def get_to_nearby_mineral_field(self, position, distance):
        return self.bot.mineral_field.closer_than(distance,position)
    
    def get_threatening_area_effects_for_position(self, position, extra_range = 0):
        effects = list(filter(lambda unit: self.filter_area_effects_for_position(unit, position, extra_range), self.bot.state.effects))
        return effects

    def filter_area_effects_for_position(self, unit, position, extra_range) -> bool:
        effects = list(filter(lambda effect: unit.id == effect.effect_id, self.bot.static_instructions.area_effects))
        if len(effects) == 0:
            return False
        return list(unit.positions)[0].distance_to(position) <= extra_range + effects[0].radius
    
    def get_exit_route_from_effects(self, start, effects):
        center = self.get_center_of_effects(effects)
        ideal_direction = start - center
        distance = 0
        while self.bot.in_map_bounds(start.towards(ideal_direction, distance)) or distance < 5:
            distance += 1
        return start.towards(ideal_direction, distance)
    
    def get_random_hidden_destination(self):
        destination = None
        for i in range(10):
            destination = self.get_random_spot()
            if (not self.bot.is_visible(destination)) and self.bot.in_pathing_grid(destination):
                break
        return destination