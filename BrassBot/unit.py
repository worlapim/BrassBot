from .tasks import Task
from .structure_or_unit import StructureOrUnit
from sc2.unit import Unit as ActualUnit
from sc2.ids.unit_typeid import UnitTypeId
from .option import Option, chose_option, chose_lowest_option

class Unit(StructureOrUnit):

    def __init__(self, bot, tag):
        super().__init__(bot, tag)

    async def on_step(self):
        if self.get_self() != None:
            threatening_area_effects = self.get_threatening_area_effects()
            if len(threatening_area_effects) > 0:
                exit = self.bot.geometry.get_exit_route_from_effects(self.get_self().position, threatening_area_effects)
                self.get_self().move(exit)
                return
            from .army_group import ArmyGroup
            if self.parent != None and type(self.parent) == ArmyGroup and self.parent.weighted_center != None and self.get_self().position.distance_to(self.parent.weighted_center) > 30:
                self.task = Task.JOINING
        await super().on_step()

    async def on_before_step(self):
        await super().on_before_step()

    async def on_after_step(self):
        await super().on_after_step()

    def update_self(self):
        actual_unit = (self.bot.units).filter(lambda unit : unit.tag == self.tag)
        if len(actual_unit) > 0:
            self.actual_unit = actual_unit[0]
            self.time_not_updated_actual_unit = 0
        else:
            self.time_not_updated_actual_unit += 1
        self.is_active = not self.get_self().is_memory

    def form_and_copy_task_from_parent(self):
        actual_self = self.get_self()
        if actual_self:
            if self.parent == None:
                nearest_army = self.nearest_army_group()
                if nearest_army:
                    self.join(nearest_army)
                else:
                    from .army_group import ArmyGroup
                    new_army = ArmyGroup(self.bot, [self])
                    self.bot.root_groups.append(new_army)
            if self.parent and self.task != Task.JOINING:
                self.task = self.parent.task
            if self.task == Task.ATTACKING and actual_self.shield_health_percentage < 0.4 and self.get_threats(3):
                self.task = Task.ATTACKING_CAREFULLY

    def do_nothing(self):
        actual_self = self.get_self()
        if self.parent:
            actual_self.attack(self.parent.center)
        else:
            actual_self.attack(actual_self.position)
            

    def do_fleeing(self):
        self.flee()

    def do_fleeing_and_gunning(self):
        self.flee_and_fire()

    def do_attacking_carefully(self):
        actual_self = self.get_self()
        if actual_self and actual_self.weapon_cooldown == 0:
            self.attack()
        else:
            self.flee()

    def go_to_center(self):
        if self.parent.weighted_center != None:
            self.get_self().move(self.parent.weighted_center)
        elif self.parent.center != None:
            self.get_self().move(self.parent.center)

    def do_attacking(self):
        self.attack()
    
    def attack(self):
        if self.parent != None and not self.can_autoattack:
            self.go_to_center()
            return
        actual_self = self.get_self()
        target = None
        if self.parent:
            target = self.parent.attacking_target
        if target:
            if type(target) == ActualUnit:
                if self.is_target_in_range(target):
                    actual_self.attack(target)
                else:
                    actual_self.attack(target.position)
            else:
                actual_self.attack(target)
        else:
            if self.parent:
                actual_self.attack(self.parent.center)
            else:
                actual_self.attack(actual_self.position)

    def lonely_attack(self, focus_fighting = True):
        if (focus_fighting or self.get_self().weapon_cooldown == 0) and len(self.get_enemies_in_range()) > 0:
            self.shoot_best_target()
        else:
            if self.bot.macro.is_structure_at_enemy_spawn:
                self.get_self().move(self.bot.enemy_start_locations[0])
            else:
                self.do_scouting()

    def do_sieging(self):
        self.siege()

    def siege(self):
        if self.parent != None and not self.can_autoattack:
            self.go_to_center()
            return
        actual_self = self.get_self()
        target = None
        if self.parent:
            target = self.parent.destination
            from_where = self.parent.weighted_center if self.parent.weighted_center else self.parent.center if self.parent.center else actual_self.position
            if target:
                if actual_self.distance_to(from_where) > len(self.parent.members)/8 + 3:
                    position_to_move_now = from_where.towards(target, 2)
                    actual_self.attack(position_to_move_now)
                else:
                    if type(target) == ActualUnit:
                        nearest_target = self.get_nearest_enemy(can_air=actual_self.can_attack_air, can_ground=actual_self.can_attack_ground, only_revealed=True)
                        if nearest_target != None and self.is_target_in_range(nearest_target) and target.is_structure and target.can_be_attacked: 
                            self.shoot_best_target()
                        elif self.is_target_in_range(target) and not target.is_structure:
                            actual_self.attack(target)
                        else:
                            actual_self.attack(target.position)
                    else:
                        actual_self.attack(target)
            else:
                actual_self.attack(self.parent.weighted_center)
        else:
            actual_self.attack(actual_self.position)

    def do_defending(self):
        self.defend()
    
    def defend(self):
        actual_unit = self.get_self()
        if actual_unit != None:
            enemy = self.get_nearest_enemy(actual_unit.can_attack_ground, actual_unit.can_attack_air, only_revealed=True)
            if enemy != None:
                actual_unit.attack(enemy)
            else:
                if self in self.bot.lonely_units:
                    actual_unit.move(actual_unit.position)
                else:
                    if self.parent.weighted_center != None:
                        actual_unit.move(self.parent.weighted_center)
                    elif self.parent.center != None:
                        actual_unit.move(self.parent.center)
                    else:
                        actual_unit.move(actual_unit.position)

    def is_target_in_range(self, target) -> bool:
        self.bot.geometry.is_target_in_range(self.get_self(), target)


    def do_scouting(self):
        actual_self = self.get_self()
        if self.parent != None and self.parent.destination != None:
            self.destination = self.parent.destination
        if self.destination == None:
            self.get_random_hidden_destination()
        elif self.bot.is_visible(self.destination) or not self.is_destination_reachable:
            self.get_random_hidden_destination()
        if len(self.get_threats(4)) > 0:
            self.flee_and_fire()
            self.destination = None
        else:
            actual_self.move(self.destination)
    
    def do_joining(self):
        actual_self = self.get_self()
        if self.parent == None:
            self.task = Task.NOTHING
            return
        if self.parent.weighted_center != None:
            if actual_self.position.distance_to(self.parent.weighted_center) > 4:
                actual_self.attack(self.parent.weighted_center)
            else:
                self.task = Task.NOTHING
        elif self.parent.center != None:
            if actual_self.position.distance_to(self.parent.center) > 4:
                actual_self.attack(self.parent.center)
            else:
                self.task = Task.NOTHING

    def flee_and_fire(self):
        actual_unit = self.get_self()
        if actual_unit and self.get_nearest_enemy():
            if actual_unit.weapon_cooldown == 0 and self.get_nearest_enemy().position.distance_to(actual_unit.position) < max(actual_unit.ground_range, actual_unit.air_range):
                self.shoot_best_target()
            else:
                self.flee()
        
    def get_random_hidden_destination(self):
        self.destination = self.bot.geometry.get_random_hidden_destination()
    
    def shoot_best_target(self):
        actual_unit = self.get_self()
        targets = self.get_enemies_in_range(actual_unit.can_attack_ground,actual_unit.can_attack_air,True,0,True)
        if len(targets) == 0:
            actual_unit.attack(actual_unit.position)
            return
        options = []
        for target in targets:
            motivation = (100 - target.shield_health_percentage)
            if not target.is_structure:
                motivation += 200
            motivation += self.bot.static_instructions.get_priority_rating_for_unit(target)
            option = Option(self.bot, motivation, target)
            options.append(option)
        target = chose_option(options).what
        actual_unit.attack(target)

        
