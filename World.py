from Utilities import *
from Player import *
from Menu import *
from Camera import *
from Player import *
from Area import *
from Static_Object import *
from Item import *
from Enemy import *
from Hud import *
from Interactive_Objects import *
from Trap import *
from Level import *

class World:
    def __init__(self):
        self.world = self.create_world()
    
    def create_world(self):
        world = {
            "1":{
                "button":BUTTON(-55, 0, 50, 50, (1, 1, 1), text="1"),
                "spawn_point":(0, 0),
                "entities":{
                    "room_list":[
                        ROOM(0, 0, 10, 10, 50, door_at='t', gap_at=""),
                        TUNNEL(10, -500, 3, 10,type='lr'),
                        TUNNEL(10, -850, 3, 3,type='t'),
                        TUNNEL(310, -850, 8, 3,type='tb'),
                        TUNNEL(-390, -850, 11, 3,type='tb'),
                        TUNNEL(-790, -850, 3, 3,type='tr'),
                        TUNNEL(-790, -600, 3, 6,type='lr'),
                        TUNNEL(-790, -350, 3, 3,type='bl'),
                        TUNNEL(-1040, -350, 5, 3,type='tb'),
                        ROOM(-1440, -350, 10, 10, door_at='l'),
                        TUNNEL(610, -850, 3, 3,type='lb'),
                        ROOM(610, -1100, 3, 6, door_at='t', gap_at='b'),
                        ROOM(610, -1500, 10, 10, door_at='btl', gap_at=''),
                        TUNNEL(1360, -1500, 20, 3, type="tb"),
                        TUNNEL(1960, -1500, 3, 3, type="tl"),
                        TUNNEL(1960, -1000, 3, 15, type="lr"),
                        TUNNEL(1960, -500, 3, 3, type="lb"),
                        TUNNEL(1710, -500, 6, 3, type="tb"),
                        ROOM(1310, -540, 10, 10, door_at='l', gap_at=''),
                        TUNNEL(630, -1850, 3, 3, type="lr"),
                        TUNNEL(630, -2050, 3, 3,type='lt'),
                        TUNNEL(130, -2050, 15, 3,type='tb'),
                        TUNNEL(-370, -2050, 3, 3,type='tr'),
                        TUNNEL(-370, -1850, 3, 3,type='lr'),
                        ROOM(-370, -1600, 10, 6,door_at='tr', gap_at=''),
                        TUNNEL(-870, -1580, 10, 3,type="tb"),
                        TUNNEL(-1220, -1580, 3, 3,type="r"),
                        TUNNEL(-1220, -1230, 3, 10,type="lr"),
                        TUNNEL(-1220, -880, 3, 3,type="bl"),
                        TUNNEL(-1570, -880, 10, 3,type="tb"),
                        ROOM(-1960, -890, 6, 15,door_at='l', gap_at=''),
                        TUNNEL(-1220, -1830, 3, 6,type="lr"),
                        ROOM(-1220, -2380, 15, 15,door_at='bt', gap_at=''),
                        ],
                    "item_list":[
                        DOOR(610, -1270, 50, callBack=updateLevel, required_key_name="0x001"),
                        KEY(-1650, -380, (1, 0, 0), name="0x001"),
                        
                        DOOR(-370, -1770, 50, callBack=updateLevel, required_key_name="0x002"),
                        KEY(1250, -530, (1, 1, 0), name="0x002"),
                        
                        DOOR(-1220, -2010, 50, callBack=updateLevel, required_key_name="0x003"),
                        KEY(-2000, -1230, (0, 1, 0), name="0x003"),
                        
                        ESCAPE_DOOR(-1220, -2800, 50, required_key_name="0x004"),
                        ],
                    "trap_list":[
                        SPIKETRAP(-740, -710, 0, 50, 30),
                        SPIKETRAP(-790, -710, 0, 50, 30),
                        SPIKETRAP(-840, -710, 0, 50, 30),
                        SPIKETRAP(-890, -710, 0, 50, 30)
                        ],
                    "static_item_list":[
                        SKULL(-880,-960, 15, 20, 20, 20, 120, False),
                        SKULL(-900,-960, 15, 20, 20, 20, 160, False),
                        SKULL(-730,-290, 15, 20, 20, 20, -45, False),
                        TORCH(-1690, -140, 0, 10, 50, 10),
                        TORCH(-1690, -610, 0, 10, 50, 10),
                        TORCH(-1160, -820, 0, 10, 50, 10),
                        TORCH(-170, -1500, 0, 10, 50, 10),
                        TORCH(-610, -1500, 0, 10, 50, 10),
                        TORCH(80, -2150, 0, 10, 50, 10),
                        SKULL(670, -790, 15, 20, 20, 20, -60, False),
                        SKULL(290, -790, 15, 20, 20, 20, -45, False),
                        SKULL(60, -590, 15, 20, 20, 20, 180, False),
                        BONE(60, -580, 0, 30, 10, 10, False),
                        BONE(50, -580, 0, 30, 10, 10, 45, False),
                        BONE(-890, -940, 0, 30, 10, 10, 45, False),
                        ],
                    "hint_arrow_list":[
                        HINT_ARROW(-10, -270, 150, 10, 10, 30),
                        HINT_ARROW(-10, -890, 150, 10, 10, 30),
                        HINT_ARROW(-800, -890, 150, 10, 10, 30),
                        HINT_ARROW(-800, -400, 150, 10, 10, 30),
                        HINT_ARROW(-1210, -340, 150, 10, 10, 30),
                        HINT_ARROW(-380, -1830, 150, 10, 10, 30),
                        HINT_ARROW(-1230, -990, 150, 10, 10, 30),
                        ],
                    "enemy_list":[
                        ZOMBIE(-1470, -530),
                        ZOMBIE(-1470, -190),
                        SKELETON(1110, -720),
                        SKELETON(1110, -380),
                        ZOMBIE(1320, -700),
                        ZOMBIE(1320, -380),
                        DOG(440, -1650),
                        DOG(610, -1730),
                        ZOMBIE(-1940, -950),
                        ZOMBIE(-2060, -600),
                        
                        ZOMBIE(-1210, -2710, items=[KEY(-940, -2720, (0, 1, 0), name="0x004"),]),
                        ZOMBIE(-1130, -2650),
                        ZOMBIE(-1310, -2650),
                        
                        SKELETON(-1590, -2620),
                        SKELETON(-900, -2450),
                        
                        DOG(-1100, -2700),
                        DOG(-1540, -2700),
                        
                        SKELETON(0, -100),
                        ],
                }
            },
            "2":{
                "button":BUTTON(0, 0, 50, 50, (1, 1, 1), text="2"),
                "spawn_point":(0, 0),
                "entities":{
                    "room_list":[
                        TUNNEL(0, -170, 3, 10, type="lrb"),
                        TUNNEL(0, -520, 3, 3, type="tl"),
                        TUNNEL(-350, -520, 10, 3, type="tb"),
                        TUNNEL(-700, -520, 3, 3, type="r"),
                        TUNNEL(-700, -20, 3, 15, type="lr"),
                        TUNNEL(-700, 480, 3, 3, type="lb"),
                        ROOM(-900, 480, 3, 3, door_at='l'),
                        TUNNEL(-700, -870, 3, 10, type="lr"),
                        TUNNEL(-700, -1220, 3, 3, type="t"),
                        TUNNEL(-200, -1220, 15, 3, type="tb"),
                        TUNNEL(300, -1220, 3, 3, type="lb"),
                        TUNNEL(300, -1470, 3, 6, type="lr"),
                        ROOM(300, -1870, 10, 10, door_at='br'),
                        TUNNEL(-1050, -1220, 10, 3, type="tb"),
                        ROOM(-1550, -1220, 10, 10, door_at='lt'),
                        TUNNEL(-1520, -1610, 3, 6, type="lr"),
                        ],
                    "item_list":[
                        KEY(280, -2065, (1, 0, 0), name="0x001")
                        ],
                    "trap_list":[
                        ],
                    "static_item_list":[
                        TORCH(0, -100, 10, 20, 60, 20)
                        ],
                    "hint_arrow_list":[
                        ],
                    "enemy_list":[
                        # SKELETON(0, -100),
                        DOG(300, -1255),
                        DOG(450, -2045),
                        DOG(100, -2045),
                        ZOMBIE(280, -1955),
                        # DOG(0, -100)
                        ],
                }
            },
            "3":{
                "button":BUTTON(-55, 0, 50, 50, (1, 1, 1), text="1"),
                "spawn_point":(0, 0),
                "entities":{
                    "room_list":[ROOM(0, 0, 10, 10, 50, door_at='t', gap_at=""),],
                    "item_list":[],
                    "trap_list":[],
                    "static_item_list":[],
                    "hint_arrow_list":[],
                    "enemy_list":[],
                }
            },
        }
        return world
    
    def load_level(self, room_no):
        global_vars.CHEAT_MODE = False 
        global_vars.SECONDS = 0
        global_vars.ROOM_LEVEL = 1

        self.world = self.create_world()
        room = self.world[room_no]

        px, py = room["spawn_point"]
        global_vars.player = ADVENTURER(px, py)
        global_vars.hud = HUD()

        entities = room["entities"]
        global_vars.room_list = entities["room_list"]
        global_vars.item_list = entities["item_list"]
        global_vars.trap_list = entities["trap_list"]
        global_vars.static_item_list = entities['static_item_list']
        global_vars.hint_arrow_list = entities['hint_arrow_list']
        global_vars.enemy_list = entities['enemy_list']
        
        pygame.mixer.music.load("audio/bg_music.mp3")
        pygame.mixer.music.play(-1)
