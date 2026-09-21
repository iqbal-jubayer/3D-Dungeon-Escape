from Utilities import *

class Level:
    def __init__(self):
        self.gamemenu = False
    
    def draw(self):
        for room in global_vars.room_list:
                room.draw()
                
        for item in global_vars.static_item_list:
            distance = math.sqrt((global_vars.player.x - item.x)**2 + (global_vars.player.y - item.y)**2)
            if distance < global_vars.DRAWING_RADIUS:
                item.draw()
                
        for item in global_vars.hint_arrow_list:
            distance = math.sqrt((global_vars.player.x - item.x)**2 + (global_vars.player.y - item.y)**2)
            if distance < global_vars.DRAWING_RADIUS and global_vars.CHEAT_MODE:
                item.draw()
            
        for item in global_vars.item_list:
            distance = math.sqrt((global_vars.player.x - item.x)**2 + (global_vars.player.y - item.y)**2)
            if distance < global_vars.DRAWING_RADIUS:
                item.draw()
            
        for trap in global_vars.trap_list:
            distance = math.sqrt((global_vars.player.x - trap.x)**2 + (global_vars.player.y - trap.y)**2)
            if distance < global_vars.DRAWING_RADIUS:
                trap.draw()
            
        for enemy in global_vars.enemy_list:
            distance = math.sqrt((global_vars.player.x - enemy.x)**2 + (global_vars.player.y - enemy.y)**2)
            if distance < global_vars.DRAWING_RADIUS:
                enemy.draw()
                
    def update(self):
        for room in global_vars.room_list:
            distance = getDistance(room.x, room.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                room.update()
        
        for item in global_vars.item_list:
            distance = getDistance(item.x, item.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                item.update()
            
        for item in global_vars.static_item_list:
            distance = getDistance(item.x, item.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                item.update()
            
        for arrow in global_vars.hint_arrow_list:
            distance = getDistance(arrow.x, arrow.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                arrow.update()
            
        for trap in global_vars.trap_list:
            distance = getDistance(trap.x, trap.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                trap.update()
            
        for enemy in global_vars.enemy_list:
            distance = getDistance(enemy.x, enemy.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
                if enemy.alive:
                    enemy.update()
                else:
                    global_vars.enemy_list.remove(enemy)
                    
    def keyboardDownListener(self, key, x, y):
        if key == b'\x1b':
            global_vars.PAUSE = not global_vars.PAUSE
            
        if global_vars.PAUSE:
            return
        
        if key == b'w':
            global_vars.player.move(1)
        if key == b's':
            global_vars.player.move(-1)
        if key == b'a':
            global_vars.player.rotate(1)
        if key == b'd':
            global_vars.player.rotate(-1)
            
        if key == b'z':
            if global_vars.player.shield > 0:
                global_vars.player.shield_on = not global_vars.player.shield_on
            
        if key == b'v':
            global_vars.VIEW_MODE = (global_vars.VIEW_MODE + 1) % 4
            
        if key == b'c':
            global_vars.CHEAT_MODE = not global_vars.CHEAT_MODE
            
        if key == b' ':
            global_vars.player.jump()
        
        for item in global_vars.item_list:
            item.keyboard_listener(key)