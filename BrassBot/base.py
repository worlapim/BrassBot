from .group import Group
from .tasks import Task
from .option import Option, chose_option, chose_lowest_option
from sc2.ids.unit_typeid import UnitTypeId

class Base(Group):
    def __init__(self, bot, members = [], base_structure = None):
        super().__init__(bot, members)
        self.mineral_fields = []
        self.workers = []
        self.base_structure = base_structure
        self.update_workers()
        self.update_mineral_fields()
        self.update_vespene_geysers()
        self.refineries = []
        self.reasign_workers()

    def build(self, structure, where):
        worker_options = []
        for worker in self.workers:
            actual_worker = worker.get_self()
            if not actual_worker:
                motivation = 0
            else:
                if structure == UnitTypeId.REFINERY:
                    motivation = (actual_worker.health + actual_worker.shield) - actual_worker.distance_to(where.position)*2
                else:
                    motivation = (actual_worker.health + actual_worker.shield) - actual_worker.distance_to(where)*2
                if actual_worker.is_carrying_resource and structure == UnitTypeId.REFINERY:
                    motivation -= 20
            if worker.task == Task.MINING:
                motivation += 50
            if worker.task == Task.GASS_MINING:
                motivation += 25
            worker_options.append(Option(self.bot, motivation, worker))
        worker = chose_option(worker_options).what
        worker.build(structure, where)
    
    def update_mineral_fields(self):
        if self.base_structure != None:
            center = self.base_structure.get_self().position
            self.mineral_fields = self.bot.mineral_field.closer_than(10,center).sorted(key=lambda patch: patch.mineral_contents, reverse = True)
    
    def update_vespene_geysers(self):
        if self.base_structure != None:
            center = self.base_structure.get_self().position
            self.vespene_geysers = self.bot.vespene_geyser.closer_than(10,center).sorted(key=lambda patch: patch.vespene_contents, reverse = True)

    def update_workers(self):
        from .scv import Scv
        from .drone import Drone
        from .probe import Probe
        workers = []
        for member in self.members:
            if type(member) == Scv or type(member) == Drone or type(member) == Probe:
                workers.append(member)
        self.workers = workers
    
    def reasign_workers(self):
        gassing_workers = []
        for worker in self.workers:
            if worker.task == Task.GASS_MINING or (worker.task == Task.FLEEING and worker.task_before_fleeing == Task.GASS_MINING):
                gassing_workers.append(worker)
        self.remove_workers_from_exhausted_refineries()
        if len(self.refineries) * 3 > len(gassing_workers) and len(self.workers) > 10:
            self.add_gassing_worker()
        #mineral_fields_amount = len(self.mineral_fields)
        mining_workers = []
        for worker in self.workers:
            if worker.task == Task.NOTHING or worker.task == Task.MINING:
                mining_workers.append(worker)
        # if (mineral_fields_amount) > 0:
        #     for i in range(len(mining_workers)):
        #         worker = mining_workers[i]
        #         self.reasign_worker(worker, self.mineral_fields[i%mineral_fields_amount])
        asigment_dictionary = self.get_mineral_asigment_dictionary()
        asigned_workers = []
        for mineral_group in asigment_dictionary.values():
            for worker in mineral_group:
                asigned_workers.append(worker)
        for worker in mining_workers:
            if worker in asigned_workers:
                continue
            options = []
            for mineral_patch in asigment_dictionary.keys():
                option = Option(self.bot, len(asigment_dictionary[mineral_patch]), mineral_patch)
                options.append(option)
            if len(options) > 0:
                mineral_patch = chose_lowest_option(options).what
                self.reasign_worker(worker, mineral_patch)
                asigment_dictionary[mineral_patch].append(worker)
                asigned_workers.append(worker)
            
    
    def get_mineral_asigment_dictionary(self) -> dict:
        asigment_dictionary = {}
        for mineral_patch in self.mineral_fields:
            asigment_dictionary[mineral_patch] = []
        for worker in self.workers:
            if worker.task != Task.MINING:
                worker.mine = None
            if worker.mine != None:
                filtered_patch = list(filter(lambda mineral_patch: mineral_patch.tag == worker.mine.tag and len(asigment_dictionary[mineral_patch]) <= 2, asigment_dictionary.keys())) #this returns sist of 1 or 0 elements
                if len(filtered_patch) > 0:
                    asigment_dictionary[filtered_patch[0]].append(worker)
        return asigment_dictionary
            
    def remove_workers_from_exhausted_refineries(self):
        for refinery in self.refineries:
            if refinery.vespene_contents == 0:
                for worker in self.workers:
                    if (worker.task == Task.GASS_MINING) and worker.vespene_mine and worker.vespene_mine.tag == refinery.tag:
                        worker.task = Task.NOTHING
                        worker.vespene_mine = None

    def get_not_full_refineries(self):
        not_full_refineries = []
        for refinery in self.refineries:
            if refinery.vespene_contents > 0:
                workers = []
                for worker in self.workers:
                    if (worker.task == Task.GASS_MINING or worker.task_before_fleeing == Task.GASS_MINING) and worker.vespene_mine and worker.vespene_mine.tag == refinery.tag:
                        workers.append(worker)
                if len(workers) < 3:
                    not_full_refineries.append(refinery)
        return not_full_refineries

    def add_gassing_worker(self):
        not_full_refineries = self.get_not_full_refineries()
        if len(not_full_refineries) > 0:
            worker_options = []
            for worker in self.workers:
                if worker.task == Task.MINING:
                    actual_worker = worker.get_self()
                    if not actual_worker:
                        motivation = 0
                    else:
                        motivation = (actual_worker.health + actual_worker.shield) - actual_worker.distance_to(not_full_refineries[0].get_self().position)*2
                        if actual_worker.is_carrying_resource:
                            motivation -= 20
                    worker_options.append(Option(self.bot, motivation, worker))
            if len(worker_options) > 0:
                worker = chose_option(worker_options).what
                worker.task = Task.GASS_MINING
                worker.vespene_mine = not_full_refineries[0]
            else:
                return False
        else:
            return False
        
    def reasign_worker(self, worker, mineral_field):
        worker.mine = mineral_field
        worker.return_structure = self.base_structure
        worker.task = Task.MINING

    def update_defenders(self):
        threats = self.get_mele_the_threads(20)
        if len(threats) <= 0:
            for worker in filter(lambda worker: worker.task == Task.DEFENDING, self.workers):
                worker.task = Task.NOTHING
        while len(threats) > 0 and len(threats) >= len(list(filter(lambda worker: worker.task == Task.DEFENDING, self.workers))) and len(self.get_candidates_workers_for_defending()) > 0:
            self.add_defending_worker(threats)

    def get_candidates_workers_for_defending(self):
        return list(filter(lambda worker: worker.task == Task.MINING or worker.task == Task.GASS_MINING or worker.task == Task.NOTHING, self.workers))

    def add_defending_worker(self, threats):
        center_of_threats = self.bot.geometry.get_center_of_units(threats)
        potential_workers = self.get_candidates_workers_for_defending()
        options = []
        for worker in potential_workers:
            actual_worker = worker.get_self()
            if actual_worker != None:
                task_motivation = 0
                if worker.task == Task.NOTHING:
                    task_motivation = 200
                elif worker.task == Task.MINING:
                    task_motivation = 100
                elif worker.task == Task.GASS_MINING:
                    task_motivation = 50
                option = Option(self.bot, 600 - actual_worker.position.distance_to(center_of_threats) + actual_worker.health + task_motivation, what= worker)
                options.append(option)
        if len(options) > 0:
            option = chose_option(options)
            option.what.task = Task.DEFENDING
            

    def add_worker(self, worker):
        worker.parent = self
        self.members.append(worker)
        self.workers.append(worker)
        self.reasign_workers()

    async def on_before_step(self):
        await super().on_before_step()
        self.update_mineral_fields()

    async def on_after_step(self):
        await super().on_after_step()

    async def on_step(self):
        if self.base_structure != None:
            if self.bot.iteration % 5 == 1:
                self.reasign_workers()
            actual_base_structure = self.base_structure.get_self()
            if actual_base_structure.is_idle:
                if actual_base_structure.type_id == UnitTypeId.COMMANDCENTER and self.bot.tech_requirement_progress(UnitTypeId.ORBITALCOMMAND) == 1:
                    if self.bot.can_afford(UnitTypeId.ORBITALCOMMAND):
                        self.base_structure.become_orbital()
                elif self.bot.can_afford(UnitTypeId.SCV) and len(self.bot.units(UnitTypeId.SCV)) <= self.bot.macro.max_workers:
                    self.base_structure.train_scv()
            if actual_base_structure.type_id == UnitTypeId.ORBITALCOMMAND and actual_base_structure.energy >= 50:
                self.base_structure.mining_mule()
        self.update_defenders()
        await super().on_step()

    async def on_unit_destroyed(self,victim):
        if await super().on_unit_destroyed(victim):
            if self.base_structure != None and await self.base_structure.on_unit_destroyed(victim):
                self.base_structure = None
                for worker in self.workers:
                    worker.return_structure = None
                return True
            for refinery in self.refineries:
                if refinery.tag == victim:
                    self.refineries.remove(refinery)
                    for worker in self.workers:
                        if worker.vespene_mine == refinery:
                            worker.vespene_mine = None
                    return True
            for worker in self.workers:
                if await worker.on_unit_destroyed(victim):
                    self.workers.remove(worker)
                    return True
    
    async def on_building_construction_complete(self, unit):
        await super().on_building_construction_complete(unit)
        from .refinery import Refinery
        if type(unit) == Refinery and self.base_structure and unit.get_self().position.distance_to(self.base_structure.get_self().position) < 10:
            self.refineries.append(unit)