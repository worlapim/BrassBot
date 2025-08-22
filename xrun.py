import sc2
import sys
from __init__ import run_ladder_game
from sc2 import Race, Difficulty, AIBuild
from sc2.player import Bot, Computer, Human

# Load bots
from bot_v1_2 import SCVPush
bot1 = Bot(Race.Terran, SCVPush())
from bronzbot_junior_v1_0 import BronzBot_junior
bot2 = Bot(Race.Terran, BronzBot_junior())
from BrassBot.brassbot import BrassBot
bot3 = Bot(Race.Terran, BrassBot())

# Start game
if __name__ == '__main__':
    if "--LadderServer" in sys.argv:
        # Ladder game started by LadderManager
        print("Starting ladder game...")
        result, opponentid = run_ladder_game(Bot(Race.Terran, BrassBot()))
        print(result, " against opponent ", opponentid)

    else:
        # Local game
        print("Starting local game...")
        #sc2.run_game(sc2.maps.get("sc2-ai-cup-2022"), [
        #sc2.run_game(sc2.maps.get("RoyalBloodAIE"), [
        sc2.run_game(sc2.maps.get("Oceanborn512V2AIE"), [
            #Human(Race.Zerg,fullscreen=True),
            Bot(sc2.Race.Terran, BrassBot(), fullscreen=True),
            #Bot(sc2.Race.Terran, BronzBot_junior())
            #Bot(sc2.Race.Terran, SCVPush()),
            Computer(sc2.Race.Random, Difficulty.Harder, ai_build=AIBuild.Macro)
        ], realtime=True)


"""
Difficulty.VeryEasy
Difficulty.Easy
Difficulty.Medium
Difficulty.MediumHard
Difficulty.Hard
Difficulty.Harder
Difficulty.VeryHard
Difficulty.CheatVision
Difficulty.CheatMoney
Difficulty.CheatInsane

AIBuild.Rush
AIBuild.Timing
AIBuild.Power
AIBuild.Macro
AIBuild.Air
AIBuild.RandomBuild
"""