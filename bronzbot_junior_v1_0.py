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

from asyncio import run



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

class BronzBot_junior(BotAI):
    NAME: str = "BronzBot jr"
    RACE: Race = Race.Terran



    def __init__(self):

        self.b_annoying_scv = self.annoying_scv

        self.b_suply = self.build_suply
        self.b_barracks = self.build_barracks
        self.b_factory = self.build_factory
        self.b_starport = self.build_starport
        self.b_refinery = self.build_refinery
        self.b_engineering = self.build_engineering_bay
        self.b_cc = self.build_command_center
        
        self.b_orbital = self.morph_orbital
        
        self.b_reaper = self.train_reaper
        self.b_marine = self.train_marine
        self.b_hellion = self.train_hellion
        self.b_viking = self.train_viking
        self.b_medivac = self.train_medivac
        
        self.b_damage = self.reaserch_damage
        self.b_armor = self.reaserch_armor
        
        self.b_annoying_scv = self.annoying_scv

        self.b_hi = self.greet
    
        self.b_haras = self.harassing_scvs
    

        self.annoying_buildorder = [
                [12, self.b_annoying_scv],
                [13, self.b_hi],
                [13, self.b_suply],
                [15, self.b_barracks],
                [15, self.b_refinery],
                [17, self.b_barracks],
                [18, self.b_reaper],
                [19, self.b_orbital],
                [19, self.b_barracks],
                [19, self.b_refinery],
                [20, self.b_reaper],
                [21, self.b_reaper],
                [22, self.b_suply],
                [23, self.b_barracks],
                [23, self.b_reaper],
                [24, self.b_reaper],
                [26, self.b_reaper],
                [27, self.b_suply],
                [29, self.b_reaper],
                [30, self.b_reaper],
                [31, self.b_reaper],
                [33, self.b_reaper],
                [35, self.b_cc],
                [35, self.b_suply]
                ]

        super().__init__()


    #-----------------------------------------------------------------------------------------------------------
    #bildorder in general
    #-----------------------------------------------------------------------------------------------------------
    def next_order(self):
            if self.buildorder != []:
                self.buildorder.pop(0)
            
    async def order(self, supply, action):
        if self.supply_used + self.dead_supply >= supply:


            #zde!!!
            await action()
        else:
            await self.make_scv()
    
    
    async def follow_buildorder(self):
        if self.buildorder != []:
            supply = self.buildorder[0][0]
            action = self.buildorder[0][1]
            await self.order(supply, action)
        else:
            self.endgame = True
    
    async def on_step(self, iteration):
        try:
            self.iteration = iteration
            self.structures
            if self.late_game == 'none':
                await self.on_before_start()
            await self.follow_buildorder()
            await self.micro_manage()
            if self.locations["enemy homes"] == []:
                await self.say_lost()
            if len(self.enemy_units(UnitTypeId.REAPER)) > 0 and len(self.units(UnitTypeId.REAPER)) > 0:
                await self.say_reaper()
            if len(self.enemy_units(UnitTypeId.SIEGETANKSIEGED)) > 0 or len(self.enemy_units(UnitTypeId.SIEGETANK)) > 0:
                await self.say_tank()
            """
            #if iteration%(60*2) == 0 and (self.dead_supply > 0 | self.dead_enemy_supply > 0):
                #await self.say("Mé ztráty: "+str(self.dead_supply))
                #await self.say("Tvé ztráty: "+str(self.dead_enemy_supply)+" (asi?)")
                
            """
        except Exception as e:
            print(iteration)
            print(e)
            await self.say_error()
    #-----------------------------------------------------------------------------------------------------------         
    #chat
    #-----------------------------------------------------------------------------------------------------------   
    async def greet(self):
        if not self.said_greet:
            greetings = ["zdar kámo","teďka si to rozdáme jako bot s botem","ahoj","tohle bude sranda","ahoj světe"]
            await self.say(greetings[random.randint(0, len(greetings)-1)])
            self.said_greet = True
        self.next_order()
    said_greet = False
        
    async def say_gg(self):
        if not self.said_gg:
            ggs = ["kruci", "to není fér", "gg", "s Pánem Bohem", "Tak se tady měj. Já jdu na jimou mapu.", "Tak nic no."]
            await self.say(ggs[random.randint(0, len(ggs)-1)])
            self.said_gg = True
    said_gg = False
    
    async def say_lost(self):
        if not self.said_lost:
            lines = ["Kam jsi šel?", "Mě se nechce hrát na schovávanou.", "Proč jsi mě opustil? :("]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_lost = True
    said_lost = False
    
    async def say_surprise(self):
        if not self.said_surprise:
            lines = ["BAF!", "Pěkný to tady máš.", "Teďka to rozjedem."]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_surprise = True
    said_surprise = False
    
    async def say_au(self):
        if not self.said_au:
            lines = ["Hej, on měl rodinu! Kdo teď nakrmí jeho děti?","Máš na rukou jeho krev. Jak se sebou budeš teď žít?","AH! To muselo bolet.", "Toho jsem měl rád. :("]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_au= True
    said_au = False
    
    async def say_reaper(self):
        if not self.said_reaper:
            lines = ["Hej, reapery tady hraju já!", "O co, že reapery umím ovládat líp než ty?"]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_reaper = True
    said_reaper = False
    
    async def say_tank(self):
        if not self.said_tank:
            lines = ["Tank! Moje jediná slabina!", "Používat tanky je podvádění.", "Ach jo... zase tanky."]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_tank = True
    said_tank = False
    
    async def say_error(self):
        if not self.said_error:
            lines = ["Můj autor je debil.", "Dneska jsem nějak zmatenej.", "Co se to děje?"]
            await self.say(lines[random.randint(0, len(lines)-1)])
            self.said_error = True
    said_error = False
    
    #-----------------------------------------------------------------------------------------------------------         
    #bildorder comands
    #-----------------------------------------------------------------------------------------------------------  
    
    
    async def make_scv(self):
        buildings = self.structures(UnitTypeId.COMMANDCENTER).idle() + self.structures(UnitTypeId.ORBITALCOMMAND).idle() + self.structures(UnitTypeId.PLANETARYFORTRESS).idle()
        if (len(buildings) > 0) & (self.minerals>=50):
            buildings[-1].train(UnitTypeId.SCV)
            
    async def build_suply(self):
        if (self.minerals >= 100) & (self.supply_workers > 0):
            loc = None
            if len(self.wall_depots_positions) > 0:
                loc = self.wall_depots_positions.pop(0)
            else:
                loc = await self.find_placement(UnitTypeId.SUPPLYDEPOT, self.get_random_home(), placement_step=3)
            worker = self.get_worker_to_build(loc)
            if worker:
                worker.build(UnitTypeId.SUPPLYDEPOT,loc)
                self.next_order()
                   
    async def build_engineering_bay(self):
        if (self.minerals >= 125) & (self.supply_workers > 0) & (self.tech_requirement_progress(UnitTypeId.ENGINEERINGBAY) == 1):
            loc = await self.find_placement(UnitTypeId.ENGINEERINGBAY, self.get_random_home(), placement_step=5)
            worker = self.get_worker_to_build(loc)
            if worker:
                worker.build(UnitTypeId.ENGINEERINGBAY,loc)
                self.next_order()
    
    async def build_command_center(self):
        if (self.minerals >= 400) & (self.supply_workers > 0):
            locations = [self.expansions["my spawn"],self.expansions["my natural"],self.expansions["my mid"],self.expansions["enemy mid"]]
            chosen = False
            for location in locations:
                buildings = self.structures(UnitTypeId.COMMANDCENTER) + self.structures(UnitTypeId.ORBITALCOMMAND) + self.structures(UnitTypeId.PLANETARYFORTRESS)
                for building in buildings:
                    if building.distance_to(location) < 2:
                        break
                else:
                    chosen = location
                    break
            chosen = await self.find_placement(UnitTypeId.COMMANDCENTER, chosen, placement_step=1)
            worker = self.get_worker_to_build(chosen)
            if worker and chosen:
                worker.build(UnitTypeId.COMMANDCENTER,chosen)
                self.next_order()
    
    async def build_dropped_command_center(self):
        if (self.minerals >= 400) & (self.supply_workers > 0):
            locations = [self.expansions["my island"],self.expansions["enemy island"]]
            chosen = False
            for location in locations:
                buildings = self.structures(UnitTypeId.COMMANDCENTER) + self.structures(UnitTypeId.ORBITALCOMMAND) + self.structures(UnitTypeId.PLANETARYFORTRESS)
                for building in buildings:
                    if building.distance_to(location) < 2:
                        break
                else:
                    for worker in self.workers:
                        if worker in self.micro["SCVs"]["dropped"] and worker.distance_to(location) < 15:
                            chosen = location
                            break
            if chosen:
                chosen = await self.find_placement(UnitTypeId.COMMANDCENTER, chosen, placement_step=1)
                worker = self.get_worker_to_build(chosen,group = "dropped")
                if worker and chosen:
                    worker.build(UnitTypeId.COMMANDCENTER,chosen)
                    self.next_order()
            else:
                self.next_order()
    
    async def build_barracks(self):
        if (self.minerals >= 150) & (self.supply_workers > 0) & (self.tech_requirement_progress(UnitTypeId.BARRACKS) == 1):
            loc = await self.find_placement(UnitTypeId.BARRACKS, self.get_random_home(), placement_step=6, addon_place=True)
            worker = self.get_worker_to_build(loc)
            if worker:
                worker.build(UnitTypeId.BARRACKS,loc)
                self.next_order()
                
    async def build_refinery(self):
        if (self.minerals >= 75) & (self.supply_workers > 0):
            buildings = self.structures(UnitTypeId.COMMANDCENTER).ready + self.structures(UnitTypeId.ORBITALCOMMAND).ready + self.structures(UnitTypeId.PLANETARYFORTRESS).ready
            geysers = []
            for building in buildings:
                if building.position.distance_to(self.expansions["my island"]) < 10 or building.position.distance_to(self.expansions["enemy island"]) < 10:
                    pass
                else:
                    geysers += self.vespene_geyser.closer_than(10,building.position)
            for geyser in geysers:
                if self.structures(UnitTypeId.REFINERY).closer_than(1,geyser.position) and geyser.has_vespene:
                    geysers.remove(geyser)
            geyser = self.chose_geyser(geysers)
            if geyser:
                worker = self.get_worker_to_build(geyser.position)
                if worker and geyser:
                    worker.build(UnitTypeId.REFINERY,geyser)
                    self.next_order()
    
    async def build_factory(self):
        if (self.minerals >= 150) & (self.vespene >= 100) & (self.supply_workers > 0) & (self.tech_requirement_progress(UnitTypeId.FACTORY) == 1):
            loc = await self.find_placement(UnitTypeId.BARRACKS, self.get_random_home(), placement_step=6, addon_place=True)
            worker = self.get_worker_to_build(loc)
            if worker:
                worker.build(UnitTypeId.FACTORY,loc)
                self.next_order()
    
    async def build_starport(self):
        if (self.minerals >= 150) & (self.vespene >= 100) & (self.supply_workers > 0) & (self.tech_requirement_progress(UnitTypeId.STARPORT) == 1):
            loc = await self.find_placement(UnitTypeId.BARRACKS, self.get_random_home(), placement_step=6, addon_place=True)
            worker = self.get_worker_to_build(loc)
            if worker:
                worker.build(UnitTypeId.STARPORT,loc)
                self.next_order()
    
    async def morph_orbital(self):
        if (self.minerals >= 150) & (self.tech_requirement_progress(UnitTypeId.ORBITALCOMMAND) == 1):
            chosen = False
            age = -1
            for cc in self.structures(UnitTypeId.COMMANDCENTER).idle():
                this_age = cc.age
                if cc.is_idle:
                    this_age += 1000
                if this_age > age:
                    chosen = cc
                    age = cc.age
            if chosen:
                chosen(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
                self.next_order()
                
    async def train_reaper(self):
        barracks = self.structures(UnitTypeId.BARRACKS).ready.idle()
        if len(barracks) > 0 and (self.minerals >= 50) & (self.vespene >= 50):
            if barracks[-1].has_reactor:
                barracks[-1].train(UnitTypeId.REAPER)
            barracks[-1].train(UnitTypeId.REAPER)
            self.next_order()
    
    async def train_marine(self):
        barracks = self.structures(UnitTypeId.BARRACKS).ready.idle()
        if len(barracks) > 0 and (self.minerals >= 50):
            if barracks[-1].has_reactor:
                barracks[-1].train(UnitTypeId.MARINE)
            barracks[-1].train(UnitTypeId.MARINE)
            self.next_order()
        
    async def train_marauder(self):
        barracks = self.structures(UnitTypeId.BARRACKS).ready.idle()
        if len(barracks) > 0 and (self.minerals >= 50):
            if barracks[-1].has_techlab:
                barracks[-1].train(UnitTypeId.MARAUDER)
            self.next_order()
            
    async def train_hellion(self):
        factories = self.structures(UnitTypeId.FACTORY).ready.idle()
        if len(factories) > 0 and (self.minerals >= 100):
            if factories[-1].has_reactor:
                factories[-1].train(UnitTypeId.HELLION)
            factories[-1].train(UnitTypeId.HELLION)
            self.next_order()  
            
    async def train_viking(self):
        starports = self.structures(UnitTypeId.STARPORT).ready.idle()
        if len(starports) > 0 and (self.minerals >= 150) & (self.vespene >= 75):
            if starports[-1].has_reactor:
                starports[-1].train(UnitTypeId.VIKINGFIGHTER)
            starports[-1].train(UnitTypeId.VIKINGFIGHTER)
            self.next_order()  
            
    async def train_medivac(self):
        starports = self.structures(UnitTypeId.STARPORT).ready.idle()
        if len(starports) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            if starports[-1].has_reactor:
                starports[-1].train(UnitTypeId.MEDIVAC)
            starports[-1].train(UnitTypeId.MEDIVAC)
            self.next_order()  
    
    async def reaserch_damage(self):
        en_bays = self.structures(UnitTypeId.ENGINEERINGBAY).ready.idle()
        if len(en_bays) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            en_bays[-1](AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1)
            self.next_order() 
    
    async def reaserch_armor(self):
        en_bays = self.structures(UnitTypeId.ENGINEERINGBAY).ready.idle()
        if len(en_bays) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            en_bays[-1](AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1 )
            self.next_order() 
            
    async def reaserch_stimpack(self):
        tech_lab = self.structures(UnitTypeId.BARRACKSTECHLAB).ready.idle()	
        if len(tech_lab) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            tech_lab[-1]( AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK )
            self.next_order() 
    
    async def reaserch_shields(self):
        tech_lab = self.structures(UnitTypeId.BARRACKSTECHLAB).ready.idle()	
        if len(tech_lab) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            tech_lab[-1]( AbilityId.RESEARCH_COMBATSHIELD )
            self.next_order() 
    
    async def reaserch_shells(self):
        tech_lab = self.structures(UnitTypeId.BARRACKSTECHLAB).ready.idle()	
        if len(tech_lab) > 0 and (self.minerals >= 50) & (self.vespene >= 50):
            tech_lab[-1]( AbilityId.RESEARCH_CONCUSSIVESHELLS )
            self.next_order() 
    
    async def reaserch_blue_flames(self):
        tech_lab = self.structures(UnitTypeId.FACTORYTECHLAB).ready.idle()	
        if len(tech_lab) > 0 and (self.minerals >= 100) & (self.vespene >= 100):
            tech_lab[-1]( AbilityId.RESEARCH_INFERNALPREIGNITER  )
            self.next_order() 
    
    async def build_reactor_barracks(self):
        barracks = self.structures(UnitTypeId.BARRACKS).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(barracks) > 0 and (self.minerals >= 50) and (self.vespene >= 50) :
            barracks[-1](AbilityId.BUILD_REACTOR_BARRACKS)
            self.next_order()
    
    async def build_reactor_factory(self):
        factories = self.structures(UnitTypeId.FACTORY).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(factories) > 0 and (self.minerals >= 50) and (self.vespene >= 50) :
            factories[-1](AbilityId.BUILD_REACTOR_FACTORY)
            self.next_order()
    
    async def build_reactor_starport(self):
        starports = self.structures(UnitTypeId.STARPORT).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(starports) > 0 and (self.minerals >= 50) and (self.vespene >= 50) :
            starports[-1](AbilityId.BUILD_REACTOR_STARPORT)
            self.next_order()
    
    async def build_techlab_barracks(self):
        barracks = self.structures(UnitTypeId.BARRACKS).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(barracks) > 0 and (self.minerals >= 50) and (self.vespene >= 25) :
            barracks[-1](AbilityId.BUILD_TECHLAB_BARRACKS)
            self.next_order()
    
    async def build_techlab_factory(self):
        factories = self.structures(UnitTypeId.FACTORY).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(factories) > 0 and (self.minerals >= 50) and (self.vespene >= 25) :
            factories[-1](AbilityId.BUILD_TECHLAB_FACTORY)
            self.next_order()
    
    async def build_techlab_starport(self):
        starports = self.structures(UnitTypeId.STARPORT).ready.idle().filter(lambda building : building.has_add_on == False)
        if len(starports) > 0 and (self.minerals >= 50) and (self.vespene >= 25) :
            starports[-1](AbilityId.BUILD_TECHLAB_STARPORT)
            self.next_order()
            
    async def annoying_scv(self):

        if len(self.micro["SCVs"]["mining"]) > 0:
           worker = self.micro["SCVs"]["mining"][0]
           self.micro["SCVs"]["mining"].remove(worker)
           self.micro["SCVs"]["annoying"].append(worker)
           worker.stop()
           self.next_order() 
    
    async def harassing_scvs(self):
        if len(self.micro["SCVs"]["mining"]) > 0:
            for worker in self.micro["SCVs"]["mining"].copy():
                self.micro["SCVs"]["mining"].remove(worker)
                self.micro["SCVs"]["harassing"].append(worker)
            self.next_order() 
    
    #-----------------------------------------------------------------------------------------------------------       
    #managment
    #-----------------------------------------------------------------------------------------------------------    
    def get_worker_to_build(self, location, group = "mining"):
        chosen = False
        distance = 10000000
        for worker in self.workers:
            if worker in self.micro["SCVs"][group]:
                this_distance = worker.position.distance_to(location)
                if worker.is_carrying_resource:
                    this_distance += 5
                if this_distance < distance:
                    chosen = worker
                    distance = this_distance
        if chosen:
            self.micro["SCVs"][group].remove(chosen)
            self.micro["SCVs"]["building"].append(chosen)
        return chosen
    
    
    def chose_geyser(self, geysers):
        if len(geysers) > 0:
            return geysers[random.randint(0, len(geysers)-1)]
        return False
      
    async def on_building_construction_complete(self,unit):
        if unit.type_id == UnitTypeId.REFINERY:
            self.gassing_wanted += 3
    
    async def on_unit_destroyed(self,victim):
        self.time_attacking = 0
        before = self.dead_supply
        self.delete_from_dict(victim,self.micro)
        if self.dead_supply > before:
            await self.say_au()
        for enemy in self.enemy_army:
            if enemy.tag == victim:
                self.enemy_army.remove(enemy)
                self.dead_enemy_supply += 1
        for enemy in self.enemy_SCVs:
            if enemy.tag == victim:
                self.enemy_SCVs.remove(enemy)
                self.dead_enemy_supply += 1
        
    def delete_from_dict(self,victim,where):
        for item in where:
            if type(where[item])==dict:
                self.delete_from_dict(victim,where[item])
            elif type(where[item])==list:
                self.delete_from_list(victim,where[item])
            elif where[item].tag == victim:
                where.remove(where[item])
                self.dead_supply += 1
                
                
    def delete_from_list(self,victim,where):
        for item in where:
            if type(item)==dict:
                self.delete_from_dict(victim,item)
            elif type(item)==list:
                self.delete_from_list(victim,item)
            elif item.tag == victim:
                where.remove(item)
                self.dead_supply += 1
    
    async def say(self, message):
        await self.chat_send(str(message))    
    #-----------------------------------------------------------------------------------------------------------       
    #micro
    #-----------------------------------------------------------------------------------------------------------    
    
    async def micro_manage(self):
        await self.check_homes()
        self.check_enemy_homes()
        self.check_mines()
        self.check_enemy_army()
        await self.micro_manage_workers()
        await self.micro_manage_buildings()
        await self.micro_manage_army()
    
    async def micro_manage_buildings(self):
        if self.dead_supply > 8:
            self.engame = True
            self.buildorder = []
        for building in self.structures_without_construction_SCVs():
            if len(self.micro["SCVs"]["mining"]) > 1:
                worker = self.micro["SCVs"]["mining"][-1]
                self.micro["SCVs"]["mining"].remove(worker)
                self.micro["SCVs"]["building"].append(worker)
                worker.smart(building)
        for orbital in self.structures(UnitTypeId.ORBITALCOMMAND).ready:
            if (orbital.energy >= 50) & (len(self.structures(UnitTypeId.ORBITALCOMMAND)) < 2) or orbital.energy >= 100:
                mineral_patches = self.mineral_field
                chosen = False
                holds = -1
                for patch in mineral_patches:
                    buildings = self.structures(UnitTypeId.COMMANDCENTER).ready + self.structures(UnitTypeId.ORBITALCOMMAND).ready + self.structures(UnitTypeId.PLANETARYFORTRESS).ready
                    for building in buildings:
                        if building.distance_to(patch.position) < 8:
                            break
                    else:
                        continue
                    if patch.mineral_contents > holds:
                        holds = patch.mineral_contents
                        chosen = patch
                if chosen:
                    orbital(AbilityId.CALLDOWNMULE_CALLDOWNMULE,chosen) 
                else:
                    orbital(AbilityId.CALLDOWNMULE_CALLDOWNMULE,self.mineral_field.closest_to(self.get_random_home()))
            elif orbital.energy >= 50:
                if self.enemy_units(UnitTypeId.SIEGETANKSIEGED).amount > 0:
                    tank = self.chose_random(self.enemy_units(UnitTypeId.SIEGETANKSIEGED))
                    targets = self.enemy_units.closer_than(12.5, tank).further_than(2, tank).not_flying()
                    if len(targets) > 0:
                        orbital(AbilityId.CALLDOWNMULE_CALLDOWNMULE,self.chose_random(targets).position)
                    else:
                       target_structures = self.enemy_structures.closer_than(12.5, tank).further_than(2, tank)
                       if len(target_structures) > 0:
                           orbital(AbilityId.CALLDOWNMULE_CALLDOWNMULE,self.chose_random(target_structures).position)
                if len(self.micro["army"]["attacking"]) > 0:
                    for guy in self.units:
                        guy_height = self.get_terrain_height(guy.position)
                        danger = False
                        for home in self.locations["enemy homes"]:
                            if guy.position.distance_to(home) < 18 and self.get_terrain_height(home) > guy_height and not self.is_on_island(home):
                                danger = home
                                break
                        if danger and guy.health > 40:
                            for friend in self.units.closer_than(10,guy.position) + self.workers.closer_than(10,guy.position):
                                if self.get_terrain_height(friend.position) > guy_height:
                                    break
                            else:
                                if 0 == len(self.units(UnitTypeId.MEDIVAC).closer_than(5,guy.position) + self.units(UnitTypeId.VIKINGFIGHTER).closer_than(5,guy.position)) and random.randint(1, 64) == 48:
                                    orbital( AbilityId.SCANNERSWEEP_SCAN, (guy.position + home)/2)
                                    break
                                
        if self.supply_used * 2.5 < len(self.enemy_army) and len(self.enemy_units.closer_than(7, self.get_random_home())) > 0:
            await self.say_gg()
            escaping = self.structures(UnitTypeId.BARRACKS) + self.structures(UnitTypeId.FACTORY) + self.structures(UnitTypeId.STARPORT)  + self.structures(UnitTypeId.ORBITALCOMMAND)  + self.structures(UnitTypeId.COMMANDCENTER)
            if len(self.structures(UnitTypeId.BARRACKS)) > 0:
               escaping.remove(self.structures(UnitTypeId.BARRACKS)[0]) 
            if len(self.structures(UnitTypeId.ORBITALCOMMAND)) > 0:
               escaping.remove(self.structures(UnitTypeId.ORBITALCOMMAND)[0]) 
            for building in escaping:
                #building.stop()
                if building.type_id == UnitTypeId.BARRACKS:
                    building( AbilityId.LIFT_BARRACKS )
                elif building.type_id == UnitTypeId.FACTORY:
                    building( AbilityId.LIFT_FACTORY )
                elif building.type_id == UnitTypeId.STARPORT:
                    building( AbilityId.LIFT_STARPORT )
            for building in self.structures(UnitTypeId.BARRACKSFLYING) + self.structures(UnitTypeId.FACTORYFLYING) + self.structures(UnitTypeId.STARPORTFLYING):
                 building.move(self.get_closest_corner(building.position))
        if self.late_game == "annoying":
            for depot in self.structures(UnitTypeId.SUPPLYDEPOT):
                if self.enemy_units().closer_than(5,depot.position).amount == 0:
                    depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER)
            for depot in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED):
                if self.enemy_units().closer_than(5,depot.position).amount > 0:
                    depot(AbilityId.MORPH_SUPPLYDEPOT_RAISE)
        if not self.endgame and self.minerals >= 1000:
            self.endgame = True
        if self.endgame:
            if self.supply_left < 4 and self.supply_cap < 200:
                await self.build_suply()
            for cc in self.structures(UnitTypeId.COMMANDCENTER).ready.idle():
                await self.morph_orbital()
            for main_hall in self.structures(UnitTypeId.COMMANDCENTER).ready.idle() + self.structures(UnitTypeId.ORBITALCOMMAND).ready.idle() + self.structures(UnitTypeId.PLANETARYFORTRESS).ready.idle():
                if len(self.units(UnitTypeId.SCV)) < 20 * len(self.structures(UnitTypeId.COMMANDCENTER) + self.structures(UnitTypeId.ORBITALCOMMAND) + self.structures(UnitTypeId.PLANETARYFORTRESS)):
                    await self.make_scv()
            if self.late_game == "annoying":
                if len(self.micro["SCVs"]["dropped"]) > 0:
                    dropped = self.micro["SCVs"]["dropped"][0]
                    if len(self.structures(UnitTypeId.COMMANDCENTER).closer_than(12,dropped.position) + self.structures(UnitTypeId.ORBITALCOMMAND).closer_than(12,dropped.position) + self.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(12,dropped.position)) == 0:
                        self.buildorder.append([0,self.build_dropped_command_center])
                        self.endgame = False
                        self.dead_supply = 0
                elif self.supply_used > 170 and self.units(UnitTypeId.VIKING).amount == 0:
                    await self.train_viking()
                    if len(self.structures(UnitTypeId.STARPORT).ready.idle()) < 2:
                        await self.build_starport()
                    if len(self.structures(UnitTypeId.FACTORY).ready.idle()) < 2:
                        await self.build_factory()
                    if len(self.structures(UnitTypeId.BARRACKS).ready.idle()) < 2:
                        await self.build_barracks()
                elif self.supply_used > 170 and self.units(UnitTypeId.MEDIVAC).amount == 0:
                    await self.train_medivac()
                    if len(self.structures(UnitTypeId.STARPORT).ready.idle()) < 2:
                        await self.build_starport()
                    if len(self.structures(UnitTypeId.FACTORY).ready.idle()) < 2:
                        await self.build_factory()
                    if len(self.structures(UnitTypeId.BARRACKS).ready.idle()) < 2:
                        await self.build_barracks()
                elif self.supply_used > 170 and self.units(UnitTypeId.MARINE).amount == 0 and self.already_pending(UnitTypeId.MARINE) == 0:
                    await self.train_marine()
                else:
                    if len(self.structures(UnitTypeId.COMMANDCENTER).ready + self.structures(UnitTypeId.ORBITALCOMMAND).ready + self.structures(UnitTypeId.PLANETARYFORTRESS).ready) > len(self.structures(UnitTypeId.REFINERY))/2:
                        await self.build_refinery()
                    await self.build_techlab_factory()
                    #await self.build_reactor_starport() #dokud se nenaučí produkovat správně s reaktorem, tohle je zbytečný
                    if len(self.structures(UnitTypeId.BARRACKS).filter(lambda building : building.has_techlab)) == 0  and self.units(UnitTypeId.MARINE).amount >= 1:
                        await self.build_techlab_barracks()
                    if len(self.micro["army"]["annoying"]) < 10 and self.vespene >= 50:
                        await self.train_reaper()
                    else:
                        for enemy in self.enemy_army:
                            if enemy.type_id == UnitTypeId.SIEGETANK or enemy.type_id == UnitTypeId.SIEGETANKSIEGED and self.vespene >= 25 and self.minerals >= 100:
                                await self.build_techlab_barracks()
                                await self.train_marauder()
                                await self.train_marine()
                                break
                        else:
                            await self.train_marine()
                    if len(self.structures(UnitTypeId.FACTORY)) < 1:
                        await self.build_factory()
                    await self.train_hellion()
                    if len(self.structures(UnitTypeId.STARPORT)) < 1:
                        await self.build_starport()
                    if self.units(UnitTypeId.MEDIVAC) == 0:
                        await self.train_medivac()
                    elif random.randint(0, 2) == 0:
                        await self.train_viking()
                    else:
                        await self.train_medivac()
                    if len(self.structures(UnitTypeId.BARRACKS)) < 4 or self.minerals > 700:
                       await self.build_barracks()
                    if len(self.structures(UnitTypeId.ENGINEERINGBAY)) < 1:
                        await self.build_engineering_bay()
                    if len(self.structures(UnitTypeId.ENGINEERINGBAY).ready.idle) > 0:
                        await self.reaserch_damage()
                        await self.reaserch_armor()
                    if self.supply_workers > 17 and len(self.structures(UnitTypeId.COMMANDCENTER) + self.structures(UnitTypeId.ORBITALCOMMAND) + self.structures(UnitTypeId.PLANETARYFORTRESS)) + self.already_pending(UnitTypeId.COMMANDCENTER) < 2:
                        await self.build_command_center()
                    if self.units(UnitTypeId.MARINE).amount >= 6:
                        await self.reaserch_shields()
                    if self.units(UnitTypeId.MARAUDER).amount >= 1:
                        await self.reaserch_shells()
                    if self.units(UnitTypeId.MARINE).amount + self.units(UnitTypeId.MARAUDER).amount >= 2:
                        await self.reaserch_stimpack()
                    if self.units(UnitTypeId.HELLION).amount >= 2:
                        await self.reaserch_blue_flames()
                
                    
                    
    
    async def micro_manage_army(self):
        if self.waiting_to_attack > 0:
            self.waiting_to_attack -= 1
        if len(self.micro["army"]["attacking"]) > 0:
            self.time_attacking += 1;
            if self.time_attacking >= 100:
                self.waiting_to_attack = 50
                for unit in self.micro["army"]["attacking"]:
                    self.micro["army"]["attacking"].remove(unit)
                    self.micro["army"]["guarding"].append(unit)
                    unit.move(unit.position)
        for unit in self.units.exclude_type({UnitTypeId.SCV, UnitTypeId.MULE}):
            if unit in self.micro["army"]["attacking"]:
                if unit.health < 30 and len(self.units(UnitTypeId.MEDIVAC).filter(lambda unit : unit.cargo_left > 1).closer_than(5, unit.position)) > 0 and unit.is_biological and len(self.enemy_units().exclude_type({UnitTypeId.MULE}).closer_than(12, unit)) > 0:
                    self.micro["army"]["attacking"].remove(unit)
                    self.micro["army"]["guarding"].append(unit)
                    medivac = self.units(UnitTypeId.MEDIVAC).filter(lambda unit : unit.cargo_left > 1).closest_to(unit.position)
                    if medivac in self.micro["army"]["supporting"]:
                        self.micro["army"]["supporting"].remove(medivac)
                        self.micro["army"]["rescuing"].append(medivac)
                    unit.smart(medivac)
                elif unit.type_id == UnitTypeId.VIKINGFIGHTER and self.enemy_structures.closer_than(4, unit).amount > 0 and self.units.closer_than(4, unit).amount > self.enemy_units.closer_than(8, unit).not_flying().amount * 1.9:
                    unit(AbilityId.MORPH_VIKINGASSAULTMODE)
                elif unit.type_id == UnitTypeId.VIKINGASSAULT and self.enemy_structures.closer_than(6, unit).amount == 0 and self.enemy_units.not_flying().closer_than(6, unit).amount == 0:
                    unit(AbilityId.MORPH_VIKINGFIGHTERMODE)
                elif unit.type_id == UnitTypeId.VIKINGFIGHTER and  self.enemy_units(UnitTypeId.MARINE).closer_than(5, unit).amount > 0 and self.enemy_units.flying().closer_than(6, unit).amount == 0:
                    unit(AbilityId.MORPH_VIKINGASSAULTMODE)
                elif len(self.enemy_structures) > 0:
                    closest_foe = self.enemy_structures.sorted_by_distance_to(unit.position)[0].position
                    if unit.type_id == UnitTypeId.VIKINGFIGHTER:
                        unit.attack(closest_foe)
                    elif self.is_on_island(unit) and self.is_on_island(closest_foe) and unit.distance_to(closest_foe) < 20 or not self.is_on_island(unit) and not self.is_on_island(closest_foe):
                        unit.attack(closest_foe)
                    elif len(self.units(UnitTypeId.MEDIVAC).filter(lambda medivac : medivac.cargo_left > 0 and medivac in self.micro["army"]["supporting"])) > 0:
                            unit.smart(self.units(UnitTypeId.MEDIVAC).filter(lambda medivac : medivac.cargo_left > 0 and medivac in self.micro["army"]["supporting"]).closest_to(unit.position))
                    elif not self.is_on_island(closest_foe):
                        unit.attack(closest_foe)
                elif len(self.units(UnitTypeId.MEDIVAC).filter(lambda medivac : medivac.cargo_left > 0 and medivac in self.micro["army"]["supporting"])) > 0:
                    unit.smart(self.units(UnitTypeId.MEDIVAC).filter(lambda medivac : medivac.cargo_left > 0 and medivac in self.micro["army"]["supporting"]).closest_to(unit.position))
                else:
                    if unit.is_idle:
                        unit.attack(self.get_random_spot())
                if self.enemy_units.closer_than(7 , unit.position).amount > 0 and unit.health >= unit.health_max - 10 and AbilityId.EFFECT_STIM_MARINE in await self.get_available_abilities(unit):
                    unit(AbilityId.EFFECT_STIM_MARINE)
                elif self.enemy_units.closer_than(7 , unit.position).not_flying().amount > 0 and unit.health >= unit.health_max - 10 and AbilityId.EFFECT_STIM_MARAUDER in await self.get_available_abilities(unit):
                    unit(AbilityId.EFFECT_STIM_MARAUDER)
            elif unit in self.micro["army"]["rescuing"]:
                if self.units.closer_than(7, unit.position).filter(lambda unit : unit.is_biological and unit.health < unit.health_max).amount > 0:
                    chosen = False
                    health = 1000000000
                    for friend in self.units.closer_than(5, unit.position).filter(lambda unit : unit.is_biological and unit.health < unit.health_max):
                        if friend.health < health:
                            health = friend.health
                            chosen = friend
                    if chosen:
                        unit.attack(chosen)
                elif unit.has_cargo and unit.distance_to(self.get_closest_home(unit.position)) > 8:
                    unit.move(self.get_closest_home(unit.position))
                elif AbilityId.UNLOADALLAT_MEDIVAC in await self.get_available_abilities(unit):
                    unit(AbilityId.UNLOADALLAT_MEDIVAC,unit.position)
                else:
                    self.micro["army"]["rescuing"].remove(unit)
                    self.micro["army"]["supporting"].append(unit)
            elif unit in self.micro["army"]["supporting"]:
                abilities = (await self.get_available_abilities(unit))
                if unit.has_cargo and (len(self.enemy_structures.closer_than(2, unit.position)) > 0) | (len(self.enemy_units(UnitTypeId.VIKINGFIGHTER).closer_than(10, unit.position)) > 0) and AbilityId.UNLOADALLAT_MEDIVAC in abilities:
                    unit(AbilityId.UNLOADALLAT_MEDIVAC,unit.position)
                elif len(self.enemy_structures) > 0 and unit.has_cargo and self.already_pending(UnitTypeId.MEDIVAC) == 0:
                    unit.attack(self.enemy_structures[-1].position)
                elif unit.has_cargo and unit.is_idle:
                    unit.move(self.get_random_corner())
                elif 0 < len(self.enemy_units(UnitTypeId.VIKINGFIGHTER).closer_than(10, unit.position) + self.enemy_units(UnitTypeId.MARINE).closer_than(10, unit.position)) and unit.is_idle:
                    unit.move(unit.position.towards(self.exit_route(unit.position, air = True),2))
                elif 0 < len(self.enemy_units(UnitTypeId.VIKINGFIGHTER).closer_than(6, unit.position) + self.enemy_units(UnitTypeId.MARINE).closer_than(6, unit.position)):
                    unit.move(unit.position.towards(self.exit_route(unit.position, air = True),1))
                else:
                    for ally in self.units.sorted_by_distance_to(unit.position):
                        if ally.is_biological and ally in self.micro["army"]["attacking"]:
                            unit.attack(ally)
                            break
                    if unit.is_idle:
                        for ally in self.units.sorted_by_distance_to(unit.position):
                            if ally.is_biological and ally.health < ally.health_max and ally in self.micro["army"]["guarding"]:
                                unit.attack(ally)
                                break
            elif unit in self.micro["army"]["dropping"]:
                space = 8 - len(self.micro["SCVs"]["being dropped"])
                for friend in self.micro["army"]["being dropped"]:
                    space -= self.calculate_supply_cost(friend.type_id)
                if len(self.micro["SCVs"]["being dropped"]) == 0 and len(self.micro["SCVs"]["mining"]) >= 10:
                    friend = self.micro["SCVs"]["mining"][-1]
                    self.micro["SCVs"]["mining"].remove(friend)
                    self.micro["SCVs"]["being dropped"].append(friend)
                for friend in self.micro["army"]["guarding"]:
                    if self.calculate_supply_cost(friend.type_id) < space - 4 and friend.type_id != UnitTypeId.VIKINGFIGHTER and friend.type_id != UnitTypeId.MEDIVAC:
                        space -= self.calculate_supply_cost(friend.type_id)
                        self.micro["army"]["guarding"].remove(friend)
                        self.micro["army"]["being dropped"].append(friend)
                        break #tehle řádek řeší snad bug s přesunutí více jednotek do "being dropped", ale ne zrovna nejelegantněji
                #await self.say(str(space) + " " + str(unit.cargo_used)+ " " + str(unit.cargo_left) + " " + str(unit.is_idle))
                if (unit.cargo_used > 0 & self.enemy_structures.closer_than(5, unit.position).amount > 0) or self.enemy_units.closer_than(6, unit.position).amount > 0:
                    unit(AbilityId.UNLOADALLAT_MEDIVAC,unit.position)
                elif unit.cargo_used > 0 and unit.cargo_left <= space and unit.is_idle or unit.cargo_left <= 1 and unit.is_idle:
                    where = random.randint(1, 2)
                    if where == 1:
                        unit(AbilityId.UNLOADALLAT_MEDIVAC,self.expansions["my island"])
                    elif where == 2:
                        unit(AbilityId.UNLOADALLAT_MEDIVAC,self.expansions["enemy island"])
                    #else:
                        #unit(AbilityId.UNLOADALLAT_MEDIVAC,(self.expansions["enemy island"] + self.expansions["my island"])/2)
            elif unit in self.micro["army"]["being dropped"]:
                dropping_medivac = False
                for medivac in self.units(UnitTypeId.MEDIVAC):
                    if medivac in self.micro["army"]["dropping"]:
                        dropping_medivac = medivac
                        break
                if self.enemy_units.closer_than(6, unit.position).amount > 0:
                    unit.attack(self.enemy_units.sorted_by_distance_to(unit.position)[0])
                elif self.enemy_structures.closer_than(8, unit.position).amount > 0:
                    unit.attack(self.enemy_structures.sorted_by_distance_to(unit.position)[0])
                elif dropping_medivac and dropping_medivac.cargo_left >= self.calculate_supply_cost(unit.type_id):
                    unit.smart(dropping_medivac)
                    dropping_medivac.smart(unit)
                else:
                    self.micro["army"]["guarding"].append(unit)
                    self.micro["army"]["being dropped"].remove(unit)
            elif unit in self.micro["army"]["guarding"]:
                threaths = self.get_threaths()
                if unit.type_id == UnitTypeId.REAPER and threaths == 0:
                    self.micro["army"]["guarding"].remove(unit)
                    self.micro["army"]["annoying"].append(unit)
                    continue
                elif unit.type_id == UnitTypeId.VIKINGFIGHTER and self.locations["enemy homes"] == [] and unit.is_idle:
                    unit.attack(self.get_random_corner())
                    continue
                if self.enemy_units.closer_than(7 , unit.position).amount > 0 and unit.health >= unit.health_max - 10 and AbilityId.EFFECT_STIM_MARINE in await self.get_available_abilities(unit):
                    unit(AbilityId.EFFECT_STIM_MARINE)
                elif self.enemy_units.closer_than(7 , unit.position).not_flying().amount > 0 and unit.health >= unit.health_max - 10 and AbilityId.EFFECT_STIM_MARAUDER in await self.get_available_abilities(unit):
                    unit(AbilityId.EFFECT_STIM_MARAUDER)
                chosen = False
                distance = 22
                for enemy in self.enemy_units().exclude_type({UnitTypeId.MULE}):
                    for home in self.locations["homes"]:
                        if home.distance_to(enemy.position) < distance:
                            distance = home.distance_to(enemy.position)
                            chosen = enemy
                if chosen:
                    unit.attack(chosen.position)
                elif len(self.units(UnitTypeId.MEDIVAC).closer_than(15, unit.position).filter(lambda unit : unit.cargo_left > 1)) > 0 and unit.health == unit.health_max:
                    medivac = self.units(UnitTypeId.MEDIVAC).closer_than(15, unit.position).filter(lambda unit : unit.cargo_left > 1)[-1]
                    unit.smart(medivac)
                    self.micro["army"]["guarding"].remove(unit)
                    self.micro["army"]["attacking"].append(unit)
                elif unit.is_idle:
                    unit.attack(self.get_random_home())
            elif unit in self.micro["army"]["annoying"]:
                abilities = (await self.get_available_abilities(unit))
                if self.enemy_units(UnitTypeId.SIEGETANKSIEGED).closer_than(12, unit.position).amount > 0:
                    target = self.enemy_units(UnitTypeId.SIEGETANKSIEGED).closest_to(unit)
                    target_location = target.position.towards(unit,1.1)
                    unit.move(target_location)
                elif unit.health < 40:
                    if len(self.enemy_units.exclude_type({UnitTypeId.MULE}).closer_than(11, unit.position)) > 0:
                        if AbilityId.KD8CHARGE_KD8CHARGE in abilities:
                            if len(self.units.closer_than(2, unit.position)) > 1:
                                if len(self.enemy_units) > 0:
                                    closest = self.enemy_units.closest_to(unit.position)
                                    if closest.distance_to(unit.position) < 5:
                                        unit(AbilityId.KD8CHARGE_KD8CHARGE, closest.position)
                            else:
                                safe_space = self.exit_route(unit.position)
                                unit.move(safe_space)
                        elif len(self.enemy_units.closer_than(7,unit.position).exclude_type({UnitTypeId.MULE, UnitTypeId.SCV})) < 2 and len(self.enemy_units.closer_than(unit.ground_range + 1,unit.position).filter(lambda foe : (foe.health < unit.health) & (foe.is_flying == False))) > 0:
                            unit.attack(self.enemy_units.filter(lambda foe : (foe.health < unit.health) & (foe.is_flying == False)).closest_to(unit.position))
                        else:
                            unit.move(unit.position.towards(self.exit_route(unit.position),10))
                    else:
                        if unit.is_idle and unit.position.y < 105 and unit.position.y > 15:
                            unit.move(self.undirect_center(unit.position, self.get_random_home(), 1))
                else:
                    if len(self.enemy_units.closer_than(15, unit.position)) == 0:
                        if unit.is_idle and len(self.units(UnitTypeId.REAPER).filter(lambda unit : unit.health >40)) * 2 > min(18,len(self.enemy_army)) or self.workers.amount <= 12:
                            destination = self.get_random_enemy_home()
                            roll = random.randint(0, 5)
                            if roll > 1:
                                unit.attack(self.undirect_goal(unit.position, destination,1.5))
                                unit.attack(destination, queue=True)
                            elif roll == 1:
                                unit.attack(self.undirect_center(unit.position, destination))
                                unit.attack(destination, queue=True)
                            else:
                                unit.attack(destination)
                        elif unit.is_idle:
                            unit.attack(unit.position.towards(self.get_random_corner(),12))
                    else:
                        from_SCV_exit = unit.position.towards(self.exit_route_from_SCVs(unit.position),2)
                        if len(self.enemy_units.closer_than(5.1, unit.position)) > 0 and AbilityId.KD8CHARGE_KD8CHARGE in abilities:
                            unit(AbilityId.KD8CHARGE_KD8CHARGE, self.enemy_units.closer_than(5.1, unit.position)[0])
                        elif len(self.enemy_units(UnitTypeId.SCV).closer_than(2, unit.position)) > 0 and self.get_terrain_height(from_SCV_exit) >= self.get_terrain_height(unit.position) and len(self.enemy_units(UnitTypeId.SCV).closer_than(2, unit.position)) >= len(self.enemy_units.exclude_type({UnitTypeId.SCV}).closer_than(8, unit.position))*1.5:
                            unit.move(from_SCV_exit)
                        elif len(self.enemy_units.exclude_type({UnitTypeId.SCV, UnitTypeId.MULE}).closer_than(7, unit.position)) > 0:
                            chosen = False
                            health = 1000000000
                            for target in self.enemy_units.exclude_type({UnitTypeId.SCV, UnitTypeId.MULE}).closer_than(7, unit.position):
                                if target.health < health:
                                    health = target.health
                                    chosen = target
                            if chosen:
                                unit.attack(chosen)
                        elif len(self.enemy_units.closer_than(10, unit.position)) > 0:
                            chosen = False
                            health = 1000000000
                            for target in self.enemy_units.closer_than(9, unit.position):
                                if target.health < health:
                                    health = target.health
                                    chosen = target
                            if chosen:
                                unit.attack(chosen)
                        else:
                            unit.attack(self.get_closest_enemy_home(unit.position))
                            
            else:
                if unit.type_id == UnitTypeId.REAPER:
                    threaths = self.get_threaths()
                    if threaths > len(self.micro["army"]["guarding"]):
                        self.micro["army"]["guarding"].append(unit)
                    else:
                        self.micro["army"]["annoying"].append(unit)
                elif unit.type_id == UnitTypeId.MEDIVAC:
                    if len(self.micro["army"]["dropping"]) == 0:
                        self.micro["army"]["dropping"].append(unit)
                    else:
                        self.micro["army"]["supporting"].append(unit)
                else:
                    self.micro["army"]["guarding"].append(unit)
            if len(self.enemy_army) < len(self.micro["army"]["guarding"] + self.micro["army"]["annoying"] + self.micro["army"]["attacking"]) - 6 and self.waiting_to_attack <= 0:
                for defender in self.micro["army"]["guarding"]:
                    self.micro["army"]["guarding"].remove(defender)
                    self.micro["army"]["attacking"].append(defender)
        
    async def micro_manage_workers(self):
        for worker in self.workers:
            if worker in self.micro["SCVs"]["mining"]:
                if worker.is_idle:
                    base = self.get_closest_mine(worker.position)
                    if base:
                        worker.gather(self.mineral_field.filter(lambda mineral : self.is_on_island(mineral) == False).closest_to(base))
                    else:
                        worker.gather(self.mineral_field.closest_to(worker))
            elif worker in self.micro["SCVs"]["defending"]:
                if worker.health <= 10 and len(self.micro["SCVs"]["mining"]) > 0:
                    self.micro["SCVs"]["defending"].remove(worker)
                    self.micro["SCVs"]["fleeing"].append(worker)
                else:
                    chosen = False
                    distance = 20
                    for enemy in self.enemy_units().exclude_type({UnitTypeId.MULE}):
                        for home in self.locations["homes"]:
                            if home.distance_to(enemy.position) < distance:
                                distance = home.distance_to(enemy.position)
                                chosen = enemy
                    if chosen:
                        worker.attack(chosen.position)
                    else:
                        self.micro["SCVs"]["defending"].remove(worker)
                        self.micro["SCVs"]["mining"].append(worker)
                        worker.stop()
            elif worker in self.micro["SCVs"]["building"]:
                if worker.is_idle:
                    self.micro["SCVs"]["building"].remove(worker)
                    self.micro["SCVs"]["mining"].append(worker)
                elif worker.is_carrying_vespene:
                    worker.stop(queue=True)
            elif worker in self.micro["SCVs"]["gassing"]:
                if worker.is_carrying_minerals or worker.is_idle:
                    for refinery in self.structures(UnitTypeId.REFINERY).ready:
                        if refinery.assigned_harvesters < 3:
                            worker.gather(refinery,queue=True)
                            break
            elif worker in self.micro["SCVs"]["annoying"]:
                if worker.is_carrying_minerals:
                    self.micro["SCVs"]["annoying"].remove(worker)
                    self.micro["SCVs"]["fleeing"].append(worker)
                    continue
                found = False
                if len(self.enemy_units.closer_than(5, worker.position)) > 0:
                    for target in self.enemy_units.closer_than(5, worker.position).sorted_by_distance_to(worker.position):
                        if target.health <= worker.health-10:
                            worker.attack(target)
                            found = True
                            break
                if found:
                    continue
                elif len(self.enemy_units.exclude_type({UnitTypeId.SCV, UnitTypeId.MULE}).closer_than(8, worker.position)) > 0 or worker.health < 15 or self.locations["enemy homes"] == []:
                    self.micro["SCVs"]["annoying"].remove(worker)
                    self.micro["SCVs"]["fleeing"].append(worker)
                elif len(self.enemy_units.closer_than(8, worker.position)) == 0:
                    worker.gather(self.mineral_field.closest_to(self.expansions['enemy spawn']))
                elif len(self.enemy_units.closer_than(3.5, worker.position)) > 1 and not found:
                    worker.gather(self.mineral_field.closest_to(self.get_closest_home(worker.position)))
                else:
                    chosen = False
                    health_distance = 1000000000
                    for foe_building in self.enemy_structures.not_ready.sorted_by_distance_to(worker.position):
                        if len(self.enemy_units(UnitTypeId.SCV)) > 0:
                            foe_constructor = self.enemy_units(UnitTypeId.SCV).closest_to(foe_building.position)
                            if foe_constructor.health * foe_constructor.position.distance_to(worker.position) < health_distance:
                                chosen = foe_constructor
                                health_distance = foe_constructor.health * foe_constructor.position.distance_to(worker.position)
                    if chosen:
                        await self.say_surprise()
                        worker.attack(chosen)
            elif worker in self.micro["SCVs"]["harassing"]:
                if worker.health < 15:
                    self.micro["SCVs"]["harassing"].remove(worker)
                    self.micro["SCVs"]["fleeing"].append(worker)
                else:
                    if self.enemy_units.closer_than(2, worker.position) == []:
                        worker.gather(self.mineral_field.closest_to(self.get_random_enemy_home()))
                    else:
                        worker.attack(worker.position)
            elif worker in self.micro["SCVs"]["fleeing"]:
                if worker.is_carrying_resource:
                    self.micro["SCVs"]["fleeing"].remove(worker)
                    self.micro["SCVs"]["mining"].append(worker)
                else:
                    worker.gather(self.mineral_field.closest_to(self.get_closest_home(worker.position)))
            elif worker in self.micro["SCVs"]["being dropped"]:
                dropping_medivac = False
                for medivac in self.units(UnitTypeId.MEDIVAC):
                    if medivac in self.micro["army"]["dropping"]:
                        dropping_medivac = medivac
                        break
                if self.enemy_units.closer_than(10, worker.position).amount > 0 and dropping_medivac:
                    worker.smart(dropping_medivac)
                elif self.enemy_structures.closer_than(10, worker.position).amount > 0:
                    worker.attack(self.enemy_structures.sorted_by_distance_to(worker.position)[0])
                elif worker.distance_to(self.expansions['my island']) < 10:
                    self.micro["SCVs"]["dropped"].append(worker)
                    self.micro["SCVs"]["being dropped"].remove(worker)
                    #ostrov
                elif worker.distance_to(self.expansions['enemy island']) < 10:
                    self.micro["SCVs"]["dropped"].append(worker)
                    self.micro["SCVs"]["being dropped"].remove(worker)
                    #ostrov
                #elif worker.distance_to((self.expansions['enemy island'] + self.expansions['my island'])/2) < 10:
                    #něco postavit na hoře
                elif dropping_medivac and dropping_medivac.cargo_left > 0:
                    worker.smart(dropping_medivac)
                    dropping_medivac.smart(worker)
                elif dropping_medivac:
                    self.micro["SCVs"]["mining"].append(worker)
                    self.micro["SCVs"]["being dropped"].remove(worker)
                    self.micro["army"]["dropping"].remove(dropping_medivac)
                    self.micro["army"]["supporting"].append(dropping_medivac)
                else:
                    self.micro["SCVs"]["mining"].append(worker)
                    self.micro["SCVs"]["being dropped"].remove(worker)
            elif worker in self.micro["SCVs"]["dropped"]:
                if len(self.structures(UnitTypeId.COMMANDCENTER).closer_than(12,worker.position) + self.structures(UnitTypeId.ORBITALCOMMAND).closer_than(12,worker.position) + self.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(12,worker.position)) == 0:
                    if worker.is_idle:
                        if worker.position.distance_to(self.expansions['enemy island']) <= 12:
                            worker.move(self.expansions['enemy island'])
                        else:
                            worker.move(self.expansions['my island'])
                else:
                    self.micro["SCVs"]["dropped"].remove(worker)
                    self.micro["SCVs"]["mining island"].append(worker)
            elif worker in self.micro["SCVs"]["mining island"]:
                if worker.is_idle:
                    worker.gather(self.mineral_field.closest_to(worker.position))
            elif worker in self.micro["SCVs"]["blocking"]:
                if self.enemy_structures().flying().closer_than(25, worker).amount > 0:
                    worker.move(self.enemy_structures().flying().closest_to(worker).position)
                else:
                    self.micro["SCVs"]["mining"].append(worker)
                    self.micro["SCVs"]["blocking"].remove(worker)
            else:
                if worker.position.distance_to(self.expansions['enemy island']) <= 12 or worker.position.distance_to(self.expansions['my island']) <= 12:
                    self.micro["SCVs"]["mining island"].append(worker)
                else:
                    self.micro["SCVs"]["mining"].append(worker)
        for building in self.structures(UnitTypeId.COMMANDCENTER).ready + self.structures(UnitTypeId.ORBITALCOMMAND).ready + self.structures(UnitTypeId.PLANETARYFORTRESS).ready:
            if building.position.distance_to(self.expansions["my island"]) < 10 or building.position.distance_to(self.expansions["enemy island"]) < 10:
                continue
            if len(self.units(UnitTypeId.SCV).closer_than(8, building.position).filter(lambda unit : unit in self.micro["SCVs"]["mining"]))/2 > len(self.mineral_field.closer_than(8, building.position)):
                chosen = False
                age = 1000000000
                for worker in self.units(UnitTypeId.SCV).closer_than(8, building.position):
                    if worker.age < age and worker in self.micro["SCVs"]["mining"] and not worker.is_carrying_resource:
                        chosen = worker
                        age = chosen.age
                if chosen and self.get_random_mine():
                    chosen.gather(self.mineral_field.closest_to(self.get_random_mine().position))
        if self.gassing_wanted > len(self.micro["SCVs"]["gassing"]) and self.vespene < 200:
            for refinery in self.structures(UnitTypeId.REFINERY).ready:
                if refinery.assigned_harvesters < 3:
                    chosen = False
                    distance = 10000000
                    for worker in self.workers:
                        if worker in self.micro["SCVs"]["mining"]:
                            this_distance = worker.position.distance_to(refinery.position)
                            if worker.is_carrying_resource:
                                this_distance += 5
                            if this_distance < distance:
                                chosen = worker
                                distance = this_distance
                    if chosen:
                        self.micro["SCVs"]["mining"].remove(chosen)
                        self.micro["SCVs"]["gassing"].append(chosen)
                        if not chosen.is_carrying_resource:
                            chosen.gather(refinery)
                        break
        elif self.gassing_wanted < len(self.micro["SCVs"]["gassing"]):
            chosen = self.micro["SCVs"]["gassing"][0]
            if chosen:
                self.micro["SCVs"]["mining"].remove(chosen)
                self.micro["SCVs"]["gassing"].append(chosen)
                if chosen.is_carrying_resource:
                    chosen.stop(queue=True)
                else:
                    chosen.move(chosen.position)
        threaths = self.get_threaths()
        closest_flying_treath = False
        distance = 1000
        flyers = self.enemy_structures().flying()
        if len(flyers) > 0:
            for home in self.locations["homes"]:
                if len(flyers) > 0:
                    mabye_closest = flyers.sorted_by_distance_to(home)[0]
                    if mabye_closest.distance_to(home) < distance:
                        distance = mabye_closest.distance_to(home)
                        closest_flying_treath = mabye_closest
        if closest_flying_treath and len(self.micro["SCVs"]["mining"]) > 2 and len(self.micro["SCVs"]["blocking"]) == 0:
            blocker = self.workers.filter(lambda scv : scv in self.micro["SCVs"]["mining"]).closest_to(closest_flying_treath)
            self.micro["SCVs"]["mining"].remove(blocker)
            self.micro["SCVs"]["blocking"].append(blocker)
        if threaths == 0:
            for worker in self.micro["SCVs"]["defending"]:
                self.micro["SCVs"]["defending"].remove(worker)
                self.micro["SCVs"]["fleeing"].append(worker)
        else:
            if len(self.micro["army"]["guarding"]) == 0:
                for i in range(threaths+1 - len(self.micro["SCVs"]["defending"])):
                    if len(self.micro["SCVs"]["mining"]) > 0:
                        worker = self.micro["SCVs"]["mining"][-1]
                        self.micro["SCVs"]["mining"].remove(worker)
                        self.micro["SCVs"]["defending"].append(worker)
                    elif len(self.micro["SCVs"]["gassing"]) > 0:
                        worker = self.micro["SCVs"]["gassing"][-1]
                        self.micro["SCVs"]["gassing"].remove(worker)
                        self.micro["SCVs"]["defending"].append(worker)
        #tenhle elif nebyl nikdy testován
                    
    
    #-----------------------------------------------------------------------------------------------------------
    #mapping
    #-----------------------------------------------------------------------------------------------------------
    def chose_random(self, group):
        count = len(group)
        return group[random.randint(0, count-1)]
    
    def get_threaths(self):
        threaths = 0
        for enemy in self.enemy_units().exclude_type({UnitTypeId.MULE}):
            for home in self.locations["homes"]:
                if home.distance_to(enemy.position) < 25:
                    threaths += 1
        return threaths
    
    def exit_route(self, location, air=False):
        enemy_locations_sum = Point2([0,0])
        enemy_locations_count = 0
        if air:
            for enemy in self.enemy_units(UnitTypeId.VIKINGFIGHTER).closer_than(10, location) + self.enemy_units(UnitTypeId.MARINE).closer_than(10, location):
                enemy_locations_sum += enemy.position
        else:
            for enemy in self.enemy_units.closer_than(10, location).exclude_type({UnitTypeId.MULE, UnitTypeId.VIKINGFIGHTER, UnitTypeId.MEDIVAC, UnitTypeId.SCV}) + self.enemy_units(UnitTypeId.SCV).closer_than(1.5, location):
                enemy_locations_sum += enemy.position
                enemy_locations_count += 1
        if enemy_locations_count == 0:
            return (self.get_closest_home(location) + location)/2
        danger_core = enemy_locations_sum / enemy_locations_count
        exit_place = location*2 - danger_core
        return exit_place
    
    def exit_route_from_SCVs(self, location):
        enemy_locations_sum = Point2([0,0])
        enemy_locations_count = 0
        for enemy in self.enemy_units(UnitTypeId.SCV).closer_than(2, location):
            enemy_locations_sum += enemy.position
            enemy_locations_count += 1
        if enemy_locations_count == 0:
            return (self.get_closest_home(location) + location)/2
        danger_core = enemy_locations_sum / enemy_locations_count
        exit_place = location*2 - danger_core
        return exit_place
    
    
    def undirect_center(self,a,b,divider = 2):
        center = (a + b) /2
        vector = center - a
        vector2 = Point2([vector.y, - vector.x])/divider
        if 0 == random.randint(0, 1):
            vector2 *= -1
        return center + vector2
    def undirect_goal(self,a,b,divider = 2):
        center = (a + b) /2
        vector = center - a
        vector2 = Point2([vector.y, - vector.x])/divider
        if 0 == random.randint(0, 1):
            vector2 *= -1
        return b + vector2
    
    def check_mines(self):
        for mine in self.mines:
            if len(self.mineral_field.closer_than(8,mine.position)) == 0: #vespene nekontroluje :(
                self.mines.remove(mine)
        for mine in self.structures(UnitTypeId.COMMANDCENTER).ready + self.structures(UnitTypeId.ORBITALCOMMAND).ready + self.structures(UnitTypeId.PLANETARYFORTRESS).ready:
            if not mine in self.mines and not mine.position.distance_to(self.expansions["my island"]) < 10 and not mine.position.distance_to(self.expansions["enemy island"]) < 10 and not len(self.mineral_field.closer_than(8,mine.position)) == 0:
                self.mines.append(mine)
    
    def check_enemy_army(self):
        see = self.enemy_units.exclude_type({UnitTypeId.SCV, UnitTypeId.MULE})
        if len(see) > len(self.enemy_army):
            self.enemy_army = see
    
    def check_enemy_SCVs(self):
        see = self.enemy_units(UnitTypeId.SCV)
        if len(see) > len(self.enemy_SCVs):
            self.enemy_SCVs = see
    
    def check_enemy_homes(self):
        for home in self.locations["enemy homes"]:
            for unit in self.units:
                if unit.distance_to(home) < 4:
                    for building in self.enemy_structures:
                        if building.distance_to(home) < 4:
                            break
                    else:
                        self.locations["enemy homes"].remove(home)
                        break
        for building in self.enemy_structures:
            for home in self.locations["enemy homes"]:
                if building.distance_to(home) < 8:
                    break
            else:
                self.locations["enemy homes"].append(building.position)
    
    async def check_homes(self):
        for home in self.locations["homes"]:
            for building in self.structures:
                if building.distance_to(home) < 12:
                    break
            else:
                self.locations["homes"].remove(home)
                break
        for building in self.structures:
            for home in self.locations["homes"]:
                if building.distance_to(home) < 12:
                    break
            else:
                self.locations["homes"].append(building.position)
    
    def get_random_enemy_home(self):
        if self.locations["enemy homes"] == []:
            return self.get_random_spot()
        return self.locations["enemy homes"][random.randint(0, len(self.locations["enemy homes"])-1)]
    
    def get_random_home(self):
        if self.locations["homes"] == []:
            return self.get_random_spot()
        return self.locations["homes"][random.randint(0, len(self.locations["homes"])-1)]
    
    def get_random_mine(self):
        if self.mines == []:
            return False
        return self.mines[random.randint(0, len(self.mines)-1)]
    
    def get_closest_enemy_home(self,location):
        chosen = False
        distance = 1000000000
        for home in self.locations["enemy homes"]:
            if location.distance_to(home) < distance:
                chosen = home
                distance = location.distance_to(home)
        if chosen:
            return chosen
        return self.get_random_spot()
    
    def get_closest_home(self,location):
        chosen = False
        distance = 1000000000
        for home in self.locations["homes"]:
            if location.distance_to(home) < distance:
                chosen = home
                distance = location.distance_to(home)
        if chosen:
            return chosen
        return self.get_random_spot()
    
    def get_closest_mine(self,location):
        chosen = False
        distance = 1000000000
        for mine in self.mines:
            if location.distance_to(mine.position) < distance:
                chosen = mine.position
                distance = location.distance_to(mine.position)
        return chosen
    
    def get_random_spot(self):
        return Point2([random.randint(0,115),random.randint(0,115)])
    
    def get_random_corner(self):
        roll = random.randint(0,3)
        return self.corners[roll]
    
    def get_closest_corner(self, location):
        chosen = False
        distance = 1000000000
        for corner in self.corners:
            if corner.distance_to(location) < distance:
                distance = corner.distance_to(location)
                chosen = corner
        return chosen
        
    def is_on_island(self, location):
        if location.distance_to(self.expansions['enemy island']) <= 13 or location.distance_to(self.expansions['my island']) <= 13:
            return True
        return False
    
    
    def make_expansion_map(self):
        if (self.enemy_start_locations[0]).position == (43.5,110.5):
            self.expansions = {
                'my spawn' : Point2([90.5,21.5]),
                'enemy spawn' : Point2([43.5,110.5]),
                'my natural' : Point2([55.5,24.5]),
                'enemy natural' : Point2([78.5,106.5]),
                'my gold' : Point2([110.5,45.5]),
                'enemy gold' : Point2([24.5,87.5]),
                'my island' : Point2([23.5,22.5]),
                'enemy island' : Point2([110.5,109.5]),
                'my mid' : Point2([49.5,66.5]),
                'enemy mid' : Point2([86.5,65.5])}
        else:
            self.expansions = {
                'enemy spawn' : Point2([90.5,21.5]),
                'my spawn' : Point2([43.5,110.5]),
                'enemy natural' : Point2([55.5,24.5]),
                'my natural' : Point2([78.5,106.5]),
                'enemy gold' : Point2([110.5,45.5]),
                'my gold' : Point2([24.5,87.5]),
                'enemy island' : Point2([23.5,22.5]),
                'my island' : Point2([110.5,109.5]),
                'enemy mid' : Point2([49.5,66.5]),
                'my mid' : Point2([86.5,65.5])}
    
    def make_3_depots_plan(self):
        if (self.enemy_start_locations[0]).position == (43.5,110.5):
            self.wall_depots_positions = [Point2([69.5,32.5]),Point2([71.5,33.5]),Point2([72.5,35.5])]
        else:
            self.wall_depots_positions = [Point2([63.5,98.5]),Point2([61.5,97.5]),Point2([60.5,95.5])]
    
    async def on_before_start(self):
        self.buildorder = self.annoying_buildorder.copy()
        #self.buildorder = self.harassing_buildorder.copy()
        self.late_game = "annoying"
        self.make_expansion_map()
        self.expansions = self.expansions.copy()
        self.locations = self.locations.copy()
        self.mines = self.mines.copy()
        
        self.locations["homes"] = [self.expansions["my spawn"].towards(self.expansions["my island"],6)]
        self.locations["enemy homes"] = [self.expansions["enemy spawn"]]
        
        self.micro = {'SCVs':{
                'flying':[],
                'attacking':[],
                'mining':[],
                'mining island':[],
                'island':[],
                'gassing':[],
                'harassing':[],
                'fleeing':[],
                'building':[],
                'annoying':[],
                'defending':[],
                'being dropped':[],
                'dropped':[],
                'blocking':[]}
            ,'army':{
                'guarding':[],
                'attacking':[],
                'annoying':[],
                'supporting':[],
                'rescuing':[],
                'mule':[],
                'dropping':[],
                'being dropped':[]}
            ,'buildings':{
                'harassing SCVs':[],
                'mining SCVs':[],
                'island SCVs':[],
                'landing':{
                    'near structure':[],
                    '':[]},
                'manual':[],
                'automatic':[]}}
        self.make_3_depots_plan()
        await self.micro_manage()

    
    #-----------------------------------------------------------------------------------------------------------       
    #variables
    #-----------------------------------------------------------------------------------------------------------       
    wall_depots_positions = []
    
    micro = {}
    
    expansions = {}
    
    locations = {}
    
    mines = []
    
    gassing_wanted = 0
    
    dead_supply = 0
    dead_enemy_supply = 0
    
    enemy_army = []
    enemy_SCVs = []
    
    endgame = False
    
    height1 = 191
    height2 = 207
    
    iteration = 0
    
    time_attacking = 0
    waiting_to_attack = 0
    
    corners = [Point2([0,0]),Point2([120,0]),Point2([0,120]), Point2([120,120])]
    
    
    # b_suply = lambda himself : run(BronzBot_junior.build_suply(himself))
    # b_barracks = lambda himself : run(BronzBot_junior.build_barracks(himself))
    # b_factory = lambda himself : run(BronzBot_junior.build_factory(himself))
    # b_starport = lambda himself : run(BronzBot_junior.build_starport(himself))
    # b_refinery = lambda himself : run(BronzBot_junior.build_refinery(himself))
    # b_engineering = lambda himself : run(BronzBot_junior.build_engineering_bay(himself))
    # b_cc = lambda himself : run(BronzBot_junior.build_command_center(himself))
    
    # b_orbital = lambda himself : run(BronzBot_junior.morph_orbital(himself))
    
    # b_reaper = lambda himself : run(BronzBot_junior.train_reaper(himself))
    # b_marine = lambda himself : run(BronzBot_junior.train_marine(himself))
    # b_hellion = lambda himself : run(BronzBot_junior.train_hellion(himself))
    # b_viking = lambda himself : run(BronzBot_junior.train_viking(himself))
    # b_medivac = lambda himself : run(BronzBot_junior.train_medivac(himself))
    
    # b_damage = lambda himself : run(BronzBot_junior.reaserch_damage(himself))
    # b_armor = lambda himself : run(BronzBot_junior.reaserch_armor(himself))
    
    # b_annoying_scv = lambda himself : run(BronzBot_junior.annoying_scv(himself))
    # b_annoying_scv = lambda himself : BronzBot_junior.annoying_scv(himself)
    #b_annoying_scv = BronzBot_junior.annoying_scv


    # b_hi = lambda himself : run(BronzBot_junior.greet(himself))
    
    # b_haras = lambda himself : run(BronzBot_junior.harassing_scvs(himself))
    
    buildorder = []
    late_game = "none"
    # harassing_buildorder = [
    #         [12,b_haras],
    #         [13,b_hi]
    #         ]
    # annoying_buildorder = [
    #           [12, b_annoying_scv],
    #           [13, b_hi],
    #           [13, b_suply],
    #           [15, b_barracks],
    #           [15, b_refinery],
    #           [17, b_barracks],
    #           [18, b_reaper],
    #           [19, b_orbital],
    #           [19, b_barracks],
    #           [19, b_refinery],
    #           [20, b_reaper],
    #           [21, b_reaper],
    #           [22, b_suply],
    #           [23, b_barracks],
    #           [23, b_reaper],
    #           [24, b_reaper],
    #           [26, b_reaper],
    #           [27, b_suply],
    #           [29, b_reaper],
    #           [30, b_reaper],
    #           [31, b_reaper],
    #           [33, b_reaper],
    #           [35, b_cc],
    #           [35, b_suply]
    #           ]
    # testing_buildorder = [
    #           [12, b_suply],
    #           [13, b_suply],
    #           [14, b_suply],
    #           [15, b_suply]
    #     ]
    
    #https://burnysc2.github.io/sc2-planner/?&race=terran&settings=tLuDriterisSritnjUrisEritm2KsIuFtN&bo=002eJyLrlbKTFGyMjHVUSqpLEhVslIqzy/KTi1SqtWByBjDJRKTSzLz8+AShpZwmeKSotLkktKiVLgkbvNwyxgZ4jHQyIDatuHyF15n4LEJERyleZkliGAyNsLnLbL9bI7L/aQ7EafTyYthMkOWRMeRERPUTrC4o4BUv1DNj7h1GFpg830sAJCIQqE=
    
    
    
    
def main():
    # Multiple difficulties for enemy bots available https://github.com/Blizzard/s2client-api/blob/ce2b3c5ac5d0c85ede96cef38ee7ee55714eeb2f/include/sc2api/sc2_gametypes.h#L30
    sc2.run_game(sc2.maps.get("sc2-ai-cup-2022"), [
        Bot(Race.Terran, BronzBot_junior()),
        Computer(Race.Terran, Difficulty.VeryHard)
    ], realtime=True)

if __name__ == '__main__':
    main()
    
    
    