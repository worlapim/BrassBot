from .unit import Unit
from .tasks import Task
from .option import Option, chose_option, chose_lowest_option
from sc2.unit import Unit as ActualUnit

class Worker(Unit):
    mine = None
    vespene_mine = None
    return_structure = None
    building_structure = None
    building_position = None
    task_before_fleeing = None
    can_place = False

    async def on_before_step(self):
        await super().on_before_step()
        worker = self.get_self()
        if worker:
            if (self.parent == None) and (self.task == Task.NOTHING):
                self.get_parent_base()
            if len(self.get_threats(extra_range=3, exclude_workers=True)) > 0 and self.task != Task.FLEEING_AND_GUNNING and self.task != Task.DEFENDING:
                self.task_before_fleeing = self.task
                self.task = Task.FLEEING_AND_GUNNING
            elif self.task == Task.FLEEING_AND_GUNNING:
                self.task = self.task_before_fleeing
                self.task_before_fleeing = None
        self.can_place = self.building_structure and self.building_position and (type(self.building_position) == ActualUnit or await self.bot.can_place_single(self.building_structure, self.building_position))

    async def on_after_step(self):
        await super().on_after_step()
    
    async def on_step(self):
        await super().on_step()
        # worker = self.get_self()
        # if worker:
        #     if self.task == Task.MINING:
        #         if worker.is_carrying_resource and self.return_structure != None:
        #             worker.smart(self.return_structure.get_self())
        #         elif self.mine != None:
        #             worker.smart(self.mine)
        #         elif len(self.bot.mineral_field) > 0:
        #             worker.smart(self.bot.mineral_field.closest_to(worker))
        #     elif self.task == Task.GASS_MINING:
        #         if worker.is_carrying_resource and self.return_structure != None:
        #             worker.smart(self.return_structure.get_self())
        #         elif self.vespene_mine != None:
        #             worker.smart(self.vespene_mine.get_self())
        #     elif self.task == Task.BUILDING and worker.is_idle:
        #         if self.bot.can_afford(self.building_structure):
        #             worker.build(self.building_structure, self.building_position)
        #         else:
        #             worker.move(self.building_position)
    
    async def on_unit_destroyed(self,victim):
        was_destroyed = await super().on_unit_destroyed(victim)
        if was_destroyed and (self.task == Task.BUILDING or self.task_before_fleeing == Task.BUILDING) and self.building_position != None and self.building_structure != None:
            base_options = []
            for base in self.bot.root_groups:
                from .base import Base
                if type(base) == Base and len(base.workers) > 0 and base.center != None:
                    base_option = Option(self.bot, base.center.distance_to(self.building_position), base)
                    base_options.append(base_option)
            if len(base_options) > 0:
                nearest_base = chose_lowest_option(base_options).what
                nearest_base.build(self.building_structure, self.building_position) 
        return was_destroyed

    def do_mining(self):
        worker = self.get_self()
        if worker.is_carrying_resource and self.return_structure != None:
            worker.smart(self.return_structure.get_self())
        elif self.mine != None:
            worker.smart(self.mine)
        elif len(self.bot.mineral_field) > 0:
            worker.smart(self.bot.mineral_field.closest_to(worker.position))

    def do_gass_mining(self):
        worker = self.get_self()
        if worker.is_carrying_resource and self.return_structure != None:
            worker.smart(self.return_structure.get_self())
        elif self.vespene_mine != None:
            worker.smart(self.vespene_mine.get_self())

    def do_building(self): #TODO není řešeno blokování pozice
        worker = self.get_self()
        structures_already_there = self.bot.structures.filter(lambda structure: structure.position.distance_to(self.building_position) <= 0)
        if structures_already_there != []:
            if structures_already_there[0].is_ready:
                self.task = Task.NOTHING
            else:
                worker.smart(structures_already_there[0])
        elif worker.is_idle:
            if self.bot.can_afford(self.building_structure):
                worker.build(self.building_structure, self.building_position)
                self.bot.is_halt_spending = False
            else:
                worker.move(self.building_position)
                if self.can_place:
                    self.bot.is_halt_spending = True

    
    def build(self, structure, where):
        self.task = Task.BUILDING
        self.building_structure = structure
        self.building_position = where
        worker = self.get_self()
        worker.build(structure, where)
    
    def get_parent_base(self):
        from .base import Base
        bases = []
        for group in self.bot.root_groups:
            if type(group) == Base:
                if group.base_structure == None:
                    bases.append(Option(self.bot,0 ,what = group))
                else:
                    try:
                        distance = group.base_structure.get_self().distance_to(self.get_self().position)
                        bases.append(Option(self.bot,1000 - distance,what = group))
                    except:
                        self.bot.chat.add_to_chat_queue("that dammed orbital error again")
        best_option = chose_option(bases)
        best_option.what.add_worker(self)