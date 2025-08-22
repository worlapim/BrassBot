from .unit import Unit
from .tasks import Task
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

class Ghost(Unit):
    
    async def on_step(self):
        if not self.bot.already_pending_upgrade(UpgradeId.PERSONALCLOAKING) == 1:
            self.form_and_copy_task_from_parent()
        else:
            if self.parent != None:
                self.leave()
            self.task = Task.ATTACKING
        await super().on_step()

    def attack(self):
        nukeable_structures = self.get_nearby_enemy_structures(12, [UnitTypeId.COMMANDCENTER, UnitTypeId.ORBITALCOMMAND, UnitTypeId.PLANETARYFORTRESS, UnitTypeId.NEXUS, UnitTypeId.HATCHERY, UnitTypeId.LAIR, UnitTypeId.HIVE], True)
        snipable_detectors = self.get_enemy_detectors_in_range(can_structure=False, bonus_range=4,only_revealed=True)
        if len(snipable_detectors) > 0 and AbilityId.EFFECT_GHOSTSNIPE in self.abilities:
            self.snipe(snipable_detectors[0])
            return
        elif self.get_self().energy >= 100 or self.parent != None:
            snipable_targets = self.get_snipeworthy_enemies_in_range()
            if len(snipable_targets) > 0 and AbilityId.EFFECT_GHOSTSNIPE in self.abilities:
                self.snipe(snipable_targets[0])
                return
        if len(self.get_threats(extra_range= 3)) > 0 and AbilityId.BEHAVIOR_CLOAKON_GHOST in self.abilities:
            self.cloak()
            return
        elif AbilityId.TACNUKESTRIKE_NUKECALLDOWN in self.abilities and len(nukeable_structures) > 0: 
            if AbilityId.BEHAVIOR_CLOAKON_GHOST in self.abilities:
                self.cloak()
                return
            else:
                self.nuke(nukeable_structures[0].position)
                return
        elif self.parent != None:
            super().attack()
        else:
            self.lonely_attack(False)

    def snipe(self, target):
        actual_unit = self.get_self()
        if AbilityId.EFFECT_GHOSTSNIPE in self.abilities:
            actual_unit(AbilityId.EFFECT_GHOSTSNIPE, target)

    def emp(self, where):
        actual_unit = self.get_self()
        if AbilityId.EMP_EMP in self.abilities:
            actual_unit(AbilityId.EMP_EMP, where)

    def cloak(self):
        actual_unit = self.get_self()
        if AbilityId.BEHAVIOR_CLOAKON_GHOST in self.abilities:
            actual_unit(AbilityId.BEHAVIOR_CLOAKON_GHOST)

    def cloakOff(self):
        actual_unit = self.get_self()
        if AbilityId.BEHAVIOR_CLOAKOFF_GHOST in self.abilities:
            actual_unit(AbilityId.BEHAVIOR_CLOAKOFF_GHOST)

    def nuke(self, where):
        actual_unit = self.get_self()
        if AbilityId.TACNUKESTRIKE_NUKECALLDOWN in self.abilities:
            actual_unit(AbilityId.TACNUKESTRIKE_NUKECALLDOWN, where)

    def get_snipeworthy_enemies_in_range(self, can_ground = True, can_air = True):
        enemies = self.get_enemies_in_range(can_ground, can_air, False, 4, True)
        targets = list(filter(lambda enemy: enemy.type_id in self.bot.static_instructions.snipe_worthy, enemies))
        return targets