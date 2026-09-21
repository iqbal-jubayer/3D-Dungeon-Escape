from Utilities import *

class HUD:
    def __init__(self):
        self.resume_button = BUTTON(0, 55, 500, 50, text="RESUME")
        self.restart_button = BUTTON(0, 0, 500, 50, text="RESTART")
        self.mainmenu_button = BUTTON(0, -55, 500, 50, text="MAINMENU")
        
    def resume_button_callback(self):
        global_vars.PAUSE = False
        
    def restart_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["SELECT WORLD"]
        global_vars.PAUSE = False
        
    def mainmenu_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
        global_vars.PAUSE = False
    
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
        bar_color = (0, 1, 0)
        if global_vars.player.health < 20:
            bar_color = (1, 0, 0)
        elif global_vars.player.health < 50:
            bar_color = (1, 1, 0)
        draw_rect(-275 - (150 - (150 * (global_vars.player.health/100)))//2, 210, 150 * (global_vars.player.health/100), 20, bar_color)
        draw_text(-350, 205, f"Player {int(global_vars.player.health)}/100")
        
    def draw_player_shield(self):
        bar_color = (0.10, 0.65, 0.75)
        draw_rect(-275 - (150 - (150 * (global_vars.player.shield/100)))//2, 185, 150 * (global_vars.player.shield/100), 20, bar_color)
        draw_text(-350, 180, f"Shield {int(global_vars.player.shield)}/100")
        
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
        
    def draw_game_menu(self):
        if not global_vars.PAUSE:
            return
        draw_rect(0, 0, WINDOW_SIZE[0]*0.8, WINDOW_SIZE[1]*0.8, color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        draw_text(-12*5, 100, "3D Dungeon Escape", font=GLUT_BITMAP_TIMES_ROMAN_24)
        self.resume_button.draw()
        self.restart_button.draw()
        self.mainmenu_button.draw()
        
    def draw(self):
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        self.draw_game_menu()
        
        self.draw_key_hud()
        self.draw_player_health()
        self.draw_player_shield()
        self.draw_fps()
        self.draw_instructions()
        self.draw_life()
        self.draw_time()
        self.draw_level_text()
        
        if global_vars.CHEAT_MODE:
            draw_text(-100, 200, "[CHEAT MODE: ON]")
            
            
        # Restore original projection and modelview matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
    
    def update(self):
        pass
    
    def mouseListener(self, button, state, x, y):
        if not global_vars.PAUSE:
            return
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.resume_button.click(x, y, self.resume_button_callback)
            self.restart_button.click(x, y, self.restart_button_callback)
            self.mainmenu_button.click(x, y, self.mainmenu_button_callback)
