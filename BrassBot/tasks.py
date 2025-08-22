import enum


class Task(enum.Enum):
    NOTHING = 0
    OTHER = 1
    MINING = 2
    GASS_MINING = 3
    BUILDING = 4
    FLEEING = 5
    FLEEING_AND_GUNNING = 6
    ATTACKING = 7
    ATTACKING_CAREFULLY = 8
    SCOUTING = 9
    SIEGING = 10
    JOINING = 11
    DEFENDING = 12


#     def __repr__(self):
#         return f"Task.{self.name}"


# for item in Task:
#     globals()[item.name] = item
