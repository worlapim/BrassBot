from .group import Group
from .tasks import Task
from sc2.position import Point2
from sc2.unit import UnitTypeId
import enum

class BuildingLineWidth(enum.Enum):
    WITHADDONS = 1
    TWOWIDE = 2
    THREEWIDE = 3

class BuildingLineGroup(Group):
    
    def __init__(self, bot, members = [], left_x = None, top_y = None, bottom_y = None, from_top = True, width = BuildingLineWidth.WITHADDONS):
        super().__init__(bot, members)
        self.left_x = left_x
        self.top_y = top_y
        self.bottom_y = bottom_y
        self.from_top = from_top
        self.width = width

    def get_step(self):
        return self.bot.geometry.get_line_step(self.width)

    async def get_next_structure_position(self):
        # print(self.__str__())
        x_center = self.left_x + 0.5
        if self.width != BuildingLineWidth.TWOWIDE:
            x_center += 0.5
        if self.from_top:
            for y_center in range(self.top_y - 1, self.bottom_y + 1, -self.get_step()):
                building_center = Point2([x_center, y_center])
                if await self.can_place_building(building_center):
                    return building_center
        else:
            for y_center in range(self.bottom_y + 1, self.top_y - 1, self.get_step()):
                building_center = Point2([x_center, y_center])
                if await self.can_place_building(building_center):
                    return building_center
    
    async def can_place_building(self, building_center):
        # print(building_center)
        if self.width == BuildingLineWidth.WITHADDONS:
            return await self.bot.geometry.can_place_building_tech_lab(building_center) and [] == self.bot.geometry.get_to_nearby_mineral_field(building_center, 6)
        elif self.width == BuildingLineWidth.TWOWIDE:
            return await self.bot.geometry.can_place_2x2(building_center) and [] == self.bot.geometry.get_to_nearby_mineral_field(building_center, 5)
        elif self.width == BuildingLineWidth.THREEWIDE:
            return await self.bot.geometry.can_place_3x3(building_center) and [] == self.bot.geometry.get_to_nearby_mineral_field(building_center, 4)

    def find_new_members(self):
        from .structure import Structure
        for loner in self.bot.lonely_units:
            actual_loner = loner.get_self()
            if (isinstance(loner, Structure) ) and (actual_loner.position.x >= self.left_x and actual_loner.position.x <= self.left_x + 4) and (actual_loner.position.y >= self.top_y and actual_loner.position.y <= self.bottom_y):
                self.members.append(loner)
                loner.parent = self
    
    def is_position_inside(self, position):
        return self.top_y > position.y and self.bottom_y < position.y and self.left_x < position.x and self.left_x + self.get_with_lenght() > position.x

    def get_building_workers(self):
        from .worker import Worker 
        building_workers = []
        for unit in self.bot.frendly_structures_or_units:
            if isinstance(unit, Worker) and (unit.task == Task.BUILDING or unit.task_before_fleeing == Task.BUILDING) and self.is_position_inside(unit.building_position) and unit.building_structure != UnitTypeId.REFINERY:
                building_workers.append(unit)
        return building_workers


    def get_with_lenght(self):
        if self.width == BuildingLineWidth.TWOWIDE:
            return 2
        if self.width == BuildingLineWidth.THREEWIDE:
            return 3
        if self.width == BuildingLineWidth.WITHADDONS:
            return 5

    async def on_before_step(self):
        self.find_new_members()
        await super().on_before_step()
        if self.center == None:
            self.center = Point2([self.left_x+1, (self.top_y+self.bottom_y)/2])

    async def on_after_step(self):
        await super().on_after_step()
    
    async def on_step(self):
        await super().on_step()

    async def on_unit_destroyed(self,victim):
        destroyed = await super().on_unit_destroyed(victim)
        if destroyed and len(self.get_building_workers()) == 0:
            self.bot.root_groups.remove(self)
        return destroyed

    def __str__(self):
     return "<BuildingLineGroup width = " + str(self.width) + ", x = " + str(self.left_x)  + ", y = " + str(self.top_y) + " - " + str(self.bottom_y) + ">"