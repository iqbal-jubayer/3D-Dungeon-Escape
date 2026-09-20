from Utilities import *

class HUD:
    def __init__(self):
        pass
    
    def draw_key_hud(self):
        draw_text(-WINDOW_SIZE[0]//2 + 10, WINDOW_SIZE[1]//2 - 100 - 20, "KEYS: ")
        for i in range(len(global_vars.player.keys)):
            x = -WINDOW_SIZE[0]//2 + 90 + i*45
            y = WINDOW_SIZE[1]//2 - 92 - 20
            draw_rect(x, y, 30, 5, color=global_vars.player.keys[i][1])
            draw_rect(x-12.5, y-5, 5, 10, color=global_vars.player.keys[i][1])
            draw_rect(x-5, y-5, 5, 10, color=global_vars.player.keys[i][1])
            draw_rect(x + 15, y, 10, 10, color=global_vars.player.keys[i][1])
            
    def draw_player_health(self):
        draw_text(-350, 205, f"Player {int(global_vars.player.health)}/100")
        bar_color = (0, 1, 0)
        if global_vars.player.health < 20:
            bar_color = (1, 0, 0)
        elif global_vars.player.health < 50:
            bar_color = (1, 1, 0)
        draw_rect(-275 - (150 - (150 * (global_vars.player.health/100)))//2, 210, 150 * (global_vars.player.health/100), 20, bar_color)
        
    def draw_player_shield(self):
        draw_text(-350, 180, f"Shield {int(global_vars.player.shield)}/100")
        bar_color = (0.10, 0.65, 0.75)
        draw_rect(-275 - (150 - (150 * (global_vars.player.shield/100)))//2, 185, 150 * (global_vars.player.shield/100), 20, bar_color)
        
    def draw_fps(self):
        fps = math.ceil(1/global_vars.dt)
        draw_text(280, 240, f"FPS: {fps}")
        
    def draw_time(self):
        s = int(global_vars.SECONDS)
        m = int(s/60)
        s = int(s%60)
        if s < 10:
            draw_text(261, 220, f"Time: {m}:0{s}")
        else:
            draw_text(261, 220, f"Time: {m}:{s}")
        
    def draw_instructions(self):
        string = "Move = w,a,s,d | Punch = L-Click | Fire = R-Click | Jump = Space"
        draw_text(-WINDOW_SIZE[0]//2+10, -WINDOW_SIZE[1]//2 + 50, string)
        string = "View = v | Interact = f | Shield = z | Sprint = L-Shift"
        draw_text(-WINDOW_SIZE[0]//2+10, -WINDOW_SIZE[1]//2 + 30, string)
        string = "Camera Z-axis = Scroll"
        draw_text(-WINDOW_SIZE[0]//2+10, -WINDOW_SIZE[1]//2 + 10, string)
        
    def draw_life(self):
        draw_text(-WINDOW_SIZE[0]//2 + 10, WINDOW_SIZE[1]//2 - 150, f"Life: {global_vars.player.life}")
        
    def draw_level_text(self):
        draw_text(265, 200, f"Level: {global_vars.ROOM_LEVEL}")
    
    def draw(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        self.draw_key_hud()
        self.draw_player_health()
        self.draw_player_shield()
        self.draw_fps()
        self.draw_instructions()
        self.draw_life()
        self.draw_time()
        self.draw_level_text()
        
        if global_vars.PAUSE:
            draw_text(-50, 0, "PAUSED")
        
        if global_vars.CHEAT_MODE:
            draw_text(-100, 200, "[CHEAT MODE: ON]")
            
            
        # Restore original projection and modelview matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def update(self):
        pass
