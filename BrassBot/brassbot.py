# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 16:50:21 2022

@author: worlapim
"""
"""
import nest_asyncio
nest_asyncio.apply()
"""
import random
import time
import asyncio

import sc2
from sc2 import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.constants import *
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.client import Client


import sc2
import sys
from sc2 import Race, Difficulty, AIBuild
from sc2.player import Bot, Computer


from .chat import Chat
from .macro import Macro
from .geometry import Geometry
from .strat import Strat
from .static_instructions import StaticInstructions
from .enemy_info import EnemyInfo
from .building_line_group import BuildingLineWidth


class BrassBot(BotAI):

    NAME: str = "BrassBot"
    RACE: Race = Race.Terran

    def __init__(self):
        super().__init__()
        self.lonely_units = []
        self.root_groups = []
        self.frendly_structures_or_units = []
        self.chat = Chat(self)
        self.macro = Macro(self)
        self.geometry = Geometry(self)
        self.strat = Strat(self)
        self.static_instructions = StaticInstructions(self)
        self.enemy_info = EnemyInfo(self)
        self.iteration = 0
        self.is_upol = None
        self.is_halt_spending = False
    
    async def on_step(self, iteration):
        # await self.chat.say(iteration)
        #start = time.time()
        self.iteration = iteration
        if iteration == 4:
            await self.chat.hello()
        #print("hello",time.time() - start)
        
        #start = time.time()
        for unit in self.lonely_units:
            await unit.on_before_step()
        #print("lonely_units",time.time() - start)
        #start = time.time()
        for group in self.root_groups:
            await group.on_before_step()
        #print("root_groups",time.time() - start)
        
        #start = time.time()
        await self.enemy_info.on_step()
        await self.strat.on_step()
        await self.macro.on_step()
        for unit in self.lonely_units:
            await unit.on_step()
        #print("lonely_units",time.time() - start)
        #start = time.time()
        for group in self.root_groups:
            await group.on_step()
        #print("root_groups",time.time() - start)

        #start = time.time()
        for unit in self.lonely_units:
            await unit.on_after_step()
        #print("lonely_units",time.time() - start)
        #start = time.time()
        for group in self.root_groups:
            await group.on_after_step()
        #print("root_groups",time.time() - start)
        #print("----")
        await self.chat.say_chat_queue()

    async def on_start(self):
        self.is_upol = self.game_info.map_name == "Sc2 AI Cup"
        self.strat.chose_strat_for_start(self.is_upol)
        self.iniciate_first_base()
        await self.macro.get_new_building_line_group(BuildingLineWidth.WITHADDONS)
        await self.macro.get_new_building_line_group(BuildingLineWidth.THREEWIDE)
        await self.macro.get_new_building_line_group(BuildingLineWidth.TWOWIDE)

    async def on_unit_destroyed(self, victim):
        #start = time.time()
        for unit in self.lonely_units:
            if await unit.on_unit_destroyed(victim):
                self.lonely_units.remove(unit)
                break
        for group in self.root_groups:
            if await group.on_unit_destroyed(victim):
                break
        for unit in self.frendly_structures_or_units:
            if unit.get_self().tag == victim:
                self.frendly_structures_or_units.remove(unit)
                break
        #print("on_unit_destroyed",time.time() - start)
        
    
    async def on_unit_created(self, actual_unit):
        #start = time.time()
        unit = self.macro.add_new_unit_to_lonely_units(actual_unit)
        if unit:
            self.frendly_structures_or_units.append(unit)
        #print("on_unit_created",time.time() - start)

    async def on_building_construction_complete(self, actual_unit):
        #start = time.time()
        unit = None
        if actual_unit.type_id == UnitTypeId.COMMANDCENTER and self.iteration > 0:
            from .base_structure import BaseStructure
            from .base import Base
            unit = BaseStructure(self, actual_unit.tag)
            base_class = Base(self, [unit], unit)
            self.root_groups.append(base_class)
        else:
            unit = await self.macro.add_new_structure_to_lonely_units(actual_structure=actual_unit)
        if unit:
            self.frendly_structures_or_units.append(unit)
            await self.macro.broadcast_new_structure(unit)
        #print("on_building_construction_complete",time.time() - start)

    def iniciate_first_base(self):
        from .base_structure import BaseStructure
        from .base import Base
        from .scv import Scv
        workers = self.workers
        base_structures = self.structures(UnitTypeId.COMMANDCENTER) + self.structures(UnitTypeId.HATCHERY) + self.structures(UnitTypeId.NEXUS)
        base_structure = base_structures[0]
        base_structure_class = BaseStructure(self,base_structure.tag)
        workers_class = []
        for worker in workers:
            workers_class.append(Scv(self,worker.tag))
        base_class = Base(self,workers_class + [base_structure_class], base_structure_class)
        self.root_groups.append(base_class)
        self.frendly_structures_or_units += workers_class
        self.frendly_structures_or_units.append(base_structure_class)
    
def main():
    # Multiple difficulties for enemy bots available https://github.com/Blizzard/s2client-api/blob/ce2b3c5ac5d0c85ede96cef38ee7ee55714eeb2f/include/sc2api/sc2_gametypes.h#L30
    sc2.run_game(sc2.maps.get("BerlingradAIE"), [
        Bot(Race.Terran, BrassBot()),
        Computer(Race.Terran, Difficulty.VeryHard)
    ], realtime=True)

if __name__ == '__main__':
    main()
    
    
    