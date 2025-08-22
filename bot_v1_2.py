# import nest_asyncio
# nest_asyncio.apply()
import random

import sc2
from sc2 import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.constants import *
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit



class SCVPush(BotAI):
    
    NAME: str = "BronzBot senior"
    RACE: Race = Race.Terran

    async def Micro(self):
        enemy_groups = self.FindEnemyGroups()
        self.MicroSCVs(enemy_groups)
        await self.MicroBuildings(enemy_groups)
        self.MicroArmy()
        
    def MicroArmy(self):
        if self.landing_timer%80==0:
            for viking in self.units(UnitTypeId.VIKINGFIGHTER):
                viking(AbilityId.MORPH_VIKINGASSAULTMODE)
        elif self.landing_timer%80==40:
            for viking in self.units(UnitTypeId.VIKINGASSAULT):
                viking(AbilityId.MORPH_VIKINGFIGHTERMODE)
        for unit in self.units.idle:
            unit.attack(self.target)
    
    async def MicroBuildings(self,enemy_groups):
        not_finished_buildings = self.structures_without_construction_SCVs()
        if not_finished_buildings:
            for SCV in self.units(UnitTypeId.SCV):
                SCV.smart(not_finished_buildings[0])
                break
            for unit in self.units.idle:
                unit.attack(not_finished_buildings[0].position)
        for building in self.structures:
            if len(self.units) * 2 < len(self.enemy_units) and len(self.enemy_units.closer_than(10, building)) > 0:
                if building.type_id == UnitTypeId.BARRACKS:
                    building(AbilityId.LIFT_BARRACKS)
                elif building.type_id == UnitTypeId.FACTORY:
                    building(AbilityId.LIFT_FACTORY)
                elif building.type_id == UnitTypeId.STARPORT:
                    building(AbilityId.LIFT_STARPORT)
                elif building.type_id == UnitTypeId.COMMANDCENTER:
                    building(AbilityId.LIFT_COMMANDCENTER)
                elif building.type_id == UnitTypeId.ORBITALCOMMAND:
                    building(AbilityId.LIFT_ORBITALCOMMAND)
                elif building.type_id == UnitTypeId.BARRACKSFLYING:
                    building.move(self.get_closest_corner(building))
                elif building.type_id == UnitTypeId.FACTORYFLYING:
                    building.move(self.get_closest_corner(building))
                elif building.type_id == UnitTypeId.STARPORTFLYING:
                    building.move(self.get_closest_corner(building))
                elif building.type_id == UnitTypeId.COMMANDCENTERFLYING:
                    building.move(self.get_closest_corner(building))
                elif building.type_id == UnitTypeId.ORBITALCOMMANDFLYING:
                    building.move(self.get_closest_corner(building))
            elif self.micro['buildings']['landing']['near structure'].count(building)==1:
                if self.enemy_structures().closer_than(5, building.position).amount > 0:
                    building(AbilityId.LAND_COMMANDCENTER, building.position)
            elif self.micro['buildings']['harassing SCVs'].count(building)==1:
                if self.can_afford(UnitTypeId.SCV) and self.harassingproduction == 0 and len(self.micro['SCVs']['harassing']) < 2:
                    self.harassingproduction += 1
                    building.train(UnitTypeId.SCV)
            elif self.micro['buildings']['mining SCVs'].count(building)==1:
                if self.can_afford(UnitTypeId.SCV) and building.is_idle and self.workers.closer_than(7, building.position).amount < 22:
                    building.train(UnitTypeId.SCV)
            elif self.micro['buildings']['island SCVs'].count(building)==1:
                if self.can_afford(UnitTypeId.SCV) and building.is_idle and self.workers.closer_than(7, building.position).amount < 22:
                    building.train(UnitTypeId.SCV)
            elif self.structures(UnitTypeId.SUPPLYDEPOT).count(building) == 1:
                building(AbilityId.MORPH_SUPPLYDEPOT_LOWER)
            
                
                        
                    
    
    def MicroSCVs(self,enemy_groups):
        gass_change = False
        for scv in self.workers:
            if self.micro['SCVs']['mining'].count(scv)==1:
                if self.structures(UnitTypeId.REFINERY).ready.amount * 3 > len(self.micro['SCVs']['gassing']):
                    self.micro['SCVs']['mining'].remove(scv)
                    self.micro['SCVs']['gassing'].insert(0,scv)
                    scv.move(scv.position)
                elif self.IsIdle(scv):
                    closest_distance=9999999
                    closest_expansion=self.expansions['my spawn']
                    for location in self.expansion_locations_dict:
                        if scv.distance_to(location) < closest_distance:
                            closest_distance = scv.distance_to(location)
                            closest_expansion = location
                    scv.gather(self.expansion_locations_dict[closest_expansion][0])
                #tahle část kódu možná přestane fungovat, až vytěžíme minerály
            elif self.micro['SCVs']['island'].count(scv)==1: 
                if self.IsIdle(scv):
                    scv.gather(self.expansion_locations_dict[self.expansions['my island']][0])
            elif self.micro['SCVs']['attacking'].count(scv)==1:
                if enemy_groups != []:
                    locations = []
                    for group in enemy_groups:
                        locations.append([])
                        for unit in group:
                            locations[-1].append(unit.position)
                    centers = []
                    for group in locations:
                        centers.append(Point2.center(group))
                    distances = []
                    for c in centers:
                        distances.append(c.distance_to(scv))
                    shortest = min(distances)
                    for i in range(len(distances)):
                        if distances[i] == shortest:
                            target = centers[i]
                    scv.attack(target)
                else:
                    scv.attack(self.expansions['enemy spawn'])
                
                    
            elif self.micro['SCVs']['flying'].count(scv)==1:
                pass
            
            elif self.micro['SCVs']['harassing'].count(scv)==1:
                if self.IsIdle(scv):
                    for building in self.structures().closer_than(10,scv.position):
                        if building.health_percentage<1:
                            scv.repair(building)
                    
            
            elif self.micro['SCVs']['building'].count(scv)==1:
                if self.IsIdle(scv):
                    self.micro['SCVs']['building'].remove(scv)
                    self.micro['SCVs']['mining'].insert(0,scv)
            elif self.micro['SCVs']['gassing'].count(scv)==1:
                if self.IsIdle(scv):
                    for refinery in self.structures(UnitTypeId.REFINERY).ready:
                        if refinery.assigned_harvesters < 3:
                            scv.gather(refinery)
                            break
                elif self.structures(UnitTypeId.REFINERY).ready.amount > 0:
                    if self.structures(UnitTypeId.REFINERY).closest_to(scv.position).assigned_harvesters > 3 and not(gass_change):
                        scv.move(scv.position)
                        gass_change = True
                    
            #doplň sem jako elif ostatní zaměření SCVček
            else:
                for building in self.structures().closer_than(5, scv.position):
                    if self.micro['buildings']['harassing SCVs'].count(building)==1:
                        self.micro['SCVs']['harassing'].insert(0,scv)
                        self.harassingproduction -=1
                        return None
                    if self.micro['buildings']['island SCVs'].count(building)==1:
                        self.micro['SCVs']['island'].insert(0,scv)
                        return None
                self.micro['SCVs']['mining'].insert(0,scv)
            
    def FindEnemyGroups(self):
        ungrouped = self.enemy_units
        groups = []
        while len(ungrouped) != 0:
            groups.insert(0,[ungrouped.pop(0)])
            while True:
                counter = 0
                for seeker in groups[0]:
                    for found in ungrouped.closer_than(4, seeker):
                        ungrouped.remove(found)
                        groups[0].append(found)
                        counter += 1
                if counter == 0:
                    break
                else:
                    counter = 0
        return groups
                
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
    
    def IsIdle(self, unit):
        for i in self.units.idle:
            if unit == i:
                return True
        return False
        
    def MakeUnit(self, unit, location, radius, number):
        if type(location) == str:
            location = self.expansions[location]
        if unit == UnitTypeId.SCV:
            if self.structures(UnitTypeId.COMMANDCENTER).sorted_by_distance_to(location).closer_than(radius, location):
                for building in self.structures(UnitTypeId.COMMANDCENTER).idle.sorted_by_distance_to(location).closer_than(radius, location):
                    if self.can_afford(unit) and number > 0:
                        number -= 1
                        building.train(unit)
                if number > 0:
                    self.buildorder.insert(0, [SCVPush.MakeUnit, unit, location, radius, number])
            else:
                self.buildorder=[]
        #Je třeba přidat další jednotky
                
                    
    async def Say(self, message):
        await self.chat_send(message)            
        
    def LoadCC(self,where,timeout):
        ccs = self.structures(UnitTypeId.COMMANDCENTERFLYING).closer_than(30, self.expansions[where])
        if ccs:
            ccs[0](AbilityId.LOADALL_COMMANDCENTER)
        else:
            if timeout > 0:
                self.buildorder.insert(0, [SCVPush.LoadCC, where, 10])
        
    def Send11SCVAttack(self):
        self.MakeExpansionMap()
        for i in range(11):
            scv=self.workers[i]
            scv.attack((self.enemy_start_locations[0]).position)
            self.micro['SCVs']['attacking'].append(scv)
        self.micro['SCVs']['flying'].append(self.workers[11])

    def SendSCV(self,where):
        self.MakeExpansionMap()
        for i in range(11):
            scv=self.workers[i]
            self.micro['SCVs']['mining'].append(scv)
        self.micro['SCVs']['harassing'].append(self.workers[11])
        self.workers[11].move(self.expansions[where])
        
    async def Build2(self, what,who,where):
        if what == UnitTypeId.REFINERY and self.can_afford(what) and len(self.micro['SCVs'][who]) > 0:
            options = self.vespene_geyser.closer_than(10,where)
            for geyser in options:
                if self.structures(UnitTypeId.REFINERY).closer_than(1,geyser.position):
                    pass
                else:
                    self.BuildIter(what,who,geyser)
                    break
        elif self.can_afford(what) and len(self.micro['SCVs'][who]) > 0 and self.tech_requirement_progress(what) == 1:
            loc = await self.find_placement(what, near=self.expansions[where])
            self.BuildIter(what,who,loc)
        else:
            self.buildorder.insert(0, ['async',SCVPush.Build2,what,who,where])
        
    async def Build(self, what,who,where,distance,aim):
        if len(self.micro['SCVs'][who]) > 0:
            if what == UnitTypeId.REFINERY and self.can_afford(what) and len(self.micro['SCVs'][who]) > 0:
                options = self.vespene_geyser.closer_than(10,self.expansions[where])
                for geyser in options:
                    if self.structures(UnitTypeId.REFINERY).closer_than(1,geyser.position):
                        pass
                    else:
                        self.BuildIter(what,who,geyser)
                        break
            elif self.can_afford(what) and len(self.micro['SCVs'][who]) > 0 and self.tech_requirement_progress(what) == 1:
                if distance == 'there':
                    self.BuildIter(what,who,self.expansions[where])
                else:
                    loc = await self.find_placement(what, near=self.expansions[where].towards(self.expansions[aim],distance))
                    if loc:
                        self.BuildIter(what,who,loc)
            else:
                self.buildorder.insert(0, ['async',SCVPush.Build,what,who,where,distance,aim])
        else:
            self.buildorder=[]
            
    def BuildIter(self,what,who,where):
        self.micro['SCVs'][who][0].build(what, where)
        if who == 'mining':
            if what == UnitTypeId.REFINERY:
                self.micro['SCVs']['gassing'].append(self.micro['SCVs'][who].pop(0))
            else:
                self.micro['SCVs']['building'].append(self.micro['SCVs'][who].pop(0))
        
    async def Planetary(self,where,radius,timer):
        wait = True
        for cc in self.structures(UnitTypeId.COMMANDCENTER).closer_than(radius,self.expansions[where]):
            abilities = await self.get_available_abilities(cc)
            if AbilityId.UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS in abilities:
                if self.can_afford(AbilityId.UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS) and cc.noqueue:
                    cc(AbilityId.UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS)
                    wait = False
                    try:
                        self.micro['buildings']['landing']['near structure'].remove(cc)
                    except:
                        pass
        if wait and timer > 0:
            self.buildorder.insert(0, ['async',SCVPush.Planetary,where,radius,timer-1])
            
        
    def LiftCC(self,where):
        if self.units(UnitTypeId.SCV).closer_than(30, self.expansions[where]):
            ccs = self.structures(UnitTypeId.COMMANDCENTER).ready.closer_than(30, self.expansions[where])
            if ccs:
                for cc in ccs:
                    cc(AbilityId.LIFT_COMMANDCENTER)
            else:
                self.buildorder.insert(0, [SCVPush.LiftCC,where])
        else:
            self.buildorder = []

    def MakeHarassingSCVs(self,where,radius):
        wait = True
        for building in self.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['harassing SCVs'].insert(0,building)
            wait = False
        if wait:
            self.buildorder.insert(0, [SCVPush.MakeHarassingSCVs,where,radius])
    
    def MakeIslandSCVs(self,where,radius):
        wait = True
        for building in self.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['island SCVs'].insert(0,building)
            wait = False
        for building in self.structures(UnitTypeId.COMMANDCENTER).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['island SCVs'].insert(0,building)
            wait = False
        for building in self.structures(UnitTypeId.ORBITALCOMMAND).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['island SCVs'].insert(0,building)
            wait = False
        if wait:
            self.buildorder.insert(0, [SCVPush.MakeMiningSCVs,where,radius])        
    
    def MakeMiningSCVs(self,where,radius):
        wait = True
        for building in self.structures(UnitTypeId.PLANETARYFORTRESS).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['mining SCVs'].insert(0,building)
            wait = False
        for building in self.structures(UnitTypeId.COMMANDCENTER).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['mining SCVs'].insert(0,building)
            wait = False
        for building in self.structures(UnitTypeId.ORBITALCOMMAND).closer_than(radius, self.expansions[where].position):
            self.micro['buildings']['mining SCVs'].insert(0,building)
            wait = False
        if wait:
            self.buildorder.insert(0, [SCVPush.MakeMiningSCVs,where,radius])
    
    def Research(self,what,timeout):
        wait = True
        if self.can_afford(what):
            self.research(what)
            wait = False
        if wait:
            timeout -= 1
            self.buildorder.insert(0, [SCVPush.Research, what, timeout])
        if timeout == 0:
            self.buildorder=[]
            
    def WaitForBank(self,m,g):
        if self.minerals >= m and self.vespene >= g:
            pass
        else:
            self.buildorder.insert(0, [SCVPush.WaitForBank, m, g])
            
    def Move(self,who1,who2,where):
        for unit in self.micro[who1][who2]:
            unit.move(self.expansions[where])
    
    """
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------------
    """

    async def Autopilot(self):
        if self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).amount < 1:
            self.Buildorder(['async',SCVPush.Build,UnitTypeId.SUPPLYDEPOT,'mining','my spawn',8,'enemy mid'])
        if self.supply_used>60 and self.target == None:
            targets = self.enemy_structures
            if targets:
                target_pos = random.randint(0,len(targets)-1)
                self.target = targets[target_pos]
                self.target_timer = 100
            else:
                for unit in self.units.idle:
                    unit.attack(Point2([random.randint(0,150),random.randint(0,150)]))
        if self.supply_workers > 15:
            for cc in self.structures(UnitTypeId.COMMANDCENTER):
                if self.structures(UnitTypeId.REFINERY).closer_than(10, cc.position).amount < 2:
                    self.Buildorder(['async',SCVPush.Build2,UnitTypeId.REFINERY,'mining',cc.position])
            if self.supply_left < 10 and self.supply_used < 190:
                self.Buildorder(['async',SCVPush.Build,UnitTypeId.SUPPLYDEPOT,'mining','my spawn',8,'my island'])
            for starport in self.structures(UnitTypeId.STARPORT):
                if starport.is_idle:
                    if self.minerals >= 150 and self.vespene >= 75:
                        starport.train(UnitTypeId.VIKINGFIGHTER)
            for factory in self.structures(UnitTypeId.FACTORY):
                if factory.is_idle:
                    if self.minerals >= 100 and self.supply_used < 120:
                        factory.train(UnitTypeId.HELLION)
            for barracks in self.structures(UnitTypeId.BARRACKS):
                if barracks.is_idle:
                    if self.minerals >= 50 and self.supply_used < 120:
                        barracks.train(UnitTypeId.MARINE)
            if self.tech_requirement_progress(UnitTypeId.ENGINEERINGBAY) == 1:
                if self.structures(UnitTypeId.ENGINEERINGBAY).amount < 1:
                    self.Buildorder(['async',SCVPush.Build,UnitTypeId.ENGINEERINGBAY,'mining','my spawn',3,'my island'])
            if self.minerals >=210 and self.vespene >= 100:
                if self.tech_requirement_progress(UnitTypeId.STARPORT) == 1:
                    if self.structures(UnitTypeId.STARPORT).amount < 6:
                        self.Buildorder(['async',SCVPush.Build,UnitTypeId.STARPORT,'mining','my spawn',11,'my natural'])
                if self.tech_requirement_progress(UnitTypeId.FACTORY) == 1:
                    if self.structures(UnitTypeId.FACTORY).amount < 3:
                        self.Buildorder(['async',SCVPush.Build,UnitTypeId.FACTORY,'mining','my spawn',8,'enemy spawn'])
            if self.tech_requirement_progress(UnitTypeId.BARRACKS) == 1:
                if self.structures(UnitTypeId.BARRACKS).amount < 3:
                    self.Buildorder(['async',SCVPush.Build,UnitTypeId.BARRACKS,'mining','my spawn',8,'enemy spawn'])
        else:
            try:
                self.train(UnitTypeId.SCV)
            except:
                pass
                
    
    def MakeExpansionMap(self):
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


    def LandCC(self,destination,how):
        self.MakeExpansionMap()
        ccs = []
        for cc in self.structures(UnitTypeId.COMMANDCENTERFLYING):
            if cc.cargo_left<5:
                ccs.append(cc)
        if ccs != []: 
            location = self.expansions.get(destination)
            ccs[0](AbilityId.LAND_COMMANDCENTER, location)
            self.micro['buildings']['landing'][how].append(ccs[0])
        else:
            self.buildorder.insert(0, [SCVPush.LandCC,destination,how])
            
    def UnloadLandedCC(self,timeout):
        wait=True
        for cc in self.structures(UnitTypeId.COMMANDCENTER):
            if cc.cargo_left<5:
                cc(AbilityId.RALLY_BUILDING,target=cc.position.towards(self.expansions['enemy island'], 1))
                cc(AbilityId.UNLOADALL_COMMANDCENTER)
                for i in range(len(self.micro['SCVs']['flying'])):
                    scv=self.micro['SCVs']['flying'].pop(0)
                    self.micro['SCVs']['mining'].insert(0,scv)
                wait=False
        if wait and timeout > 0:
            self.buildorder.insert(0, [SCVPush.UnloadLandedCC, timeout - 1])
        if timeout <= 0:
            self.buildorder=[]
            
    def ChangeSCV(self,source,to,number):
        for scv in self.micro["SCVs"][source]:
            if number > 0:
                self.micro['SCVs'][source].remove(scv)
                self.micro['SCVs'][to].insert(0,scv)
                number -= 1
            else:
                return None
        self.buildorder.insert(0, [SCVPush.ChangeSCV,source,to,number])
       
    def Buildorder(self,addition):
        self.buildorder.insert(0, addition)
    
    async def FollowBuildorder(self):
        if self.buildorder != []:
            current_task = self.buildorder.pop(0)
            if current_task[0]!='async':
                if len(current_task)==1:
                    current_task[0](self)
                elif len(current_task)==2:
                    current_task[0](self,current_task[1])
                elif len(current_task)==3:
                    current_task[0](self,current_task[1], current_task[2])
                elif len(current_task)==4:
                    current_task[0](self,current_task[1], current_task[2], current_task[3])
                elif len(current_task)==5:
                    current_task[0](self,current_task[1], current_task[2], current_task[3], current_task[4])
            else:
                if len(current_task)==2:
                    await current_task[1](self)
                elif len(current_task)==3:
                    await current_task[1](self,current_task[2])
                elif len(current_task)==4:
                    await current_task[1](self,current_task[2] ,current_task[3])
                elif len(current_task)==5:
                    await current_task[1](self,current_task[2] ,current_task[3], current_task[4])
                elif len(current_task)==6:
                    await current_task[1](self,current_task[2] ,current_task[3], current_task[4], current_task[5])
                elif len(current_task)==7:
                    await current_task[1](self,current_task[2] ,current_task[3], current_task[4], current_task[5], current_task[6])
                    
            #Rozšířit tohle, pokud bude potřeba více argumentů v buildorderu
                
    async def on_unit_destroyed(self,victim):
        self.DeleteFromDict(victim,self.micro)
        if self.target:
            if self.target.tag == victim:
                self.target = None
                
    
    def DeleteFromDict(self,victim,where):
        for item in where:
            if type(where[item])==dict:
                self.DeleteFromDict(victim,where[item])
            elif type(where[item])==list:
                self.DeleteFromList(victim,where[item])
            elif where[item].tag == victim:
                where.remove(where[item])
                
                
    def DeleteFromList(self,victim,where):
        for item in where:
            if type(item)==dict:
                self.DeleteFromDict(victim,item)
            elif type(item)==list:
                self.DeleteFromList(victim,item)
            elif item.tag == victim:
                where.remove(item)
        
        
        
    async def on_step(self, iteration):
        #print(self.buildorder)
        if self.buildorder == []:
            self.buildorder = [['async', SCVPush.Autopilot]]
        await self.FollowBuildorder()
        await self.Micro()
        self.landing_timer += 1
        if self.target_timer > 0:
            self.target_timer -= 1
        else:
            self.target = None
        
    async def on_before_start(self):
        self.MakeExpansionMap()
        self.buildorder = self.planetaryrush.copy()
        #self.buildorder = self.scvrush.copy()
        self.expansions = self.expansions.copy()
        self.micro = {'SCVs':{
                'flying':[],
                'attacking':[],
                'mining':[],
                'island':[],
                'gassing':[],
                'harassing':[],
                'building':[]}
            ,'army':{
                'guarding':[],
                'attacking':[]}
            ,'buildings':{
                'harassing SCVs':[],
                'mining SCVs':[],
                'island SCVs':[],
                'landing':{
                    'near structure':[],
                    '':[]},
                'manual':[],
                'automatic':[]}}
        
    
    async def on_unit_took_damage(self, unit, amount_damage_taken):
        if unit.is_mine:
            for defence in self.units.idle:
                if defence not in self.units(UnitTypeId.SCV):
                    defence.attack(unit.position)
            for defence in self.units.closer_than(15, unit.position):
                if self.micro['SCVs']['harassing'].count(defence) != 1:
                    defence.attack(unit.position)
            if self.landing_timer < 140 or self.supply_used < 8:
                self.buildorder = []
                self.micro['SCVs']['harassing']=[]
                for building in self.structures:
                    try:
                        building(AbilityId.CANCEL)
                    except:
                        pass
                    
    
        
        
    expansions = {}
        
    micro = {}  


    scvrush = [[Send11SCVAttack],
                  [LiftCC,'my spawn'],
                  [LoadCC,'my spawn',10],
                  [LandCC,'enemy island',''],
                  ['async', Say, 'Ahoj'],
                  [UnloadLandedCC,1000],
                  [MakeUnit, UnitTypeId.SCV, 'enemy island', 1, 14]]
    
    planetaryrush = [[SendSCV,"enemy natural"], 
                   ['async', Say, 'Ahoj'],
                   ['async',Build,UnitTypeId.COMMANDCENTER,'harassing','enemy natural',"there",None],
                   ['async',Build,UnitTypeId.REFINERY,'mining','my spawn',"there",None],
                   [MakeUnit, UnitTypeId.SCV, 'my spawn', 1, 1],
                   ['async',Build,UnitTypeId.ENGINEERINGBAY,'mining','my spawn',3,'my island'],
                   ['async',Build,UnitTypeId.REFINERY,'mining','my spawn',"there",None],
                   [MakeUnit, UnitTypeId.SCV, 'my spawn', 1, 3],
                   [LiftCC,'enemy natural'],
                   [LoadCC,'enemy natural',10],
                   [LandCC,'enemy spawn','near structure'],
                   [UnloadLandedCC,80],
                   ['async',Planetary,'enemy spawn',80,10],
                   ['async',Planetary,'my spawn',1,200],
                   [MakeHarassingSCVs,'enemy spawn',80],
                   [Research,UpgradeId.HISECAUTOTRACKING,80],
                   [MakeMiningSCVs,'my spawn',1],
                   [ChangeSCV,"mining","flying",1],
                   ['async',Build,UnitTypeId.COMMANDCENTER,'flying','my island',20,'my mid'],
                   ['async',Build,UnitTypeId.SUPPLYDEPOT,'mining','my spawn',5,'enemy mid'],
                   ['async',Build,UnitTypeId.BARRACKS,'mining','my spawn',5,'my island'],
                   ['async',Build,UnitTypeId.FACTORY,'mining','my spawn',10,'my island'],
                   ['async',Build,UnitTypeId.FACTORY,'mining','my spawn',10,'my island'],
                   ['async',Build,UnitTypeId.FACTORY,'mining','my spawn',10,'my island'],
                   [LiftCC,'my island'],
                   [LoadCC,'my island',10],
                   [LandCC,'my island',''],
                   [UnloadLandedCC,80],
                   ['async',Planetary,'my island',1,200],
                   [MakeIslandSCVs,'my island',1]]
     
    justplay=[[MakeMiningSCVs, 'my spawn', 2]]
       
    buildorder = []
    
    harassingproduction=0
    
    target = None
    target_timer = 0
    landing_timer = 0
    
    corners = [Point2([0,0]),Point2([120,0]),Point2([0,120]), Point2([120,120])]



