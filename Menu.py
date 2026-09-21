from Utilities import *

class MainMenu:
    def __init__(self):
        self.start_button = BUTTON(0, 100, 500, 50, text="START")
        self.help_button =  BUTTON(0, 40, 500, 50, text="HELP")
        self.credits_button = BUTTON(0, -20, 500, 50, text="CREDITS")
        self.exit_button =  BUTTON(0, -80, 500, 50, text="EXIT")
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        draw_text(-12*5, 200, "3D Dungeon Escape", font=GLUT_BITMAP_TIMES_ROMAN_24)
        self.start_button.draw()
        self.help_button.draw()
        self.credits_button.draw()
        self.exit_button.draw()
        
    def start_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["SELECT WORLD"]
        
    def help_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["HELP"]
        
    def credits_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["CREDITS"]
        
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.start_button.click(x, y, self.start_button_callback)
            self.help_button.click(x,y,self.help_button_callback)
            self.credits_button.click(x,y,self.credits_button_callback)
            self.exit_button.click(x,y, glutLeaveMainLoop)

class RoomMenu:
    def __init__(self):
        # print(game_init)
        self.room_buttons = [
            BUTTON(-55, 0, 50, 50, (1, 1, 1), text="1"),
            BUTTON(0, 0, 50, 50, (1, 1, 1), text="2"),
        ]
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        draw_text(-100, WINDOW_SIZE[1]//2 - 100, "SELECT WORLD", font=GLUT_BITMAP_TIMES_ROMAN_24)
        
        for button in self.room_buttons:
            button.draw()
            
    def room_button_callback(self, room):
        global_vars.SELECTED_WORLD = room
    
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            for i, button in enumerate(self.room_buttons):
                button.click(x, y, self.room_button_callback, f"{i+1}")

class HelpMenu:
    def __init__(self):
        self.back_button =  BUTTON(-WINDOW_SIZE[0]//2 + 40, WINDOW_SIZE[1]//2 - 100, 100, 30, text="Back")
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        
        draw_text(0, WINDOW_SIZE[1]//2 - 100, "HELP", font=GLUT_BITMAP_TIMES_ROMAN_24)
        self.back_button.draw()
        
    def back_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
    
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.back_button.click(x, y, self.back_button_callback)

class EscapeMenu:
    def __init__(self):
        self.mainmenu_button =  BUTTON(0, 40, 500, 50, text="MAINMENU")
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        
        end_quote = "A NEW LIFE BEGINS"
        draw_text(-6*len(end_quote), 140, end_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
        s = int(global_vars.SECONDS)
        m = int(s/60)
        s = int(s%60)
        if s < 10:
            time_quote = f"Time: {m}:0{s}"
        else:
            time_quote = f"Time: {m}:{s}"
        draw_text(-6*len(time_quote), 110, time_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
        self.mainmenu_button.draw()
        
    def mainmenu_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
    
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.mainmenu_button.click(x, y, self.mainmenu_button_callback)
            
class GameOverMenu:
    def __init__(self):
        self.mainmenu_button =  BUTTON(0, 40, 500, 50, text="MAINMENU")
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        
        end_quote = "GAME OVER!"
        draw_text(-6*len(end_quote), 100, end_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
        self.mainmenu_button.draw()
        
    def mainmenu_button_callback(self):
            global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
    
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.mainmenu_button.click(x, y, self.mainmenu_button_callback)
            
class CreditsMenu:
    def __init__(self):
        self.back_button =  BUTTON(20, -170, 100, 30, text="Back")
    
    def draw(self):
        glColor4f(1, 0, 0, 1)
        draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
        
        draw_text(-20, WINDOW_SIZE[1]//2 - 100, "CREDITS", font=GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(-50, 100, "[CSE423 - LAB]", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(-100, 60, "COMPUTER GRAPHICS", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(-50, 10, "DEVELOPED BY,", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(0, -30, "JUBAYER IQBAL", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(0, -70, "YEASIN ARAFAT RABBY", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(0, -110, "MD. ATIKULLA TANVIR", font=GLUT_BITMAP_HELVETICA_18)
        self.back_button.draw()
        
    def back_button_callback(self):
        global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
    
    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            self.back_button.click(x, y, self.back_button_callback)

class Menu:
    def __init__(self):
        self.mainMenu = MainMenu()
        self.helpMenu = HelpMenu()
        self.creditsMenu = CreditsMenu()
        self.roomMenu = RoomMenu()
        self.escapeMenu = EscapeMenu()
        self.gameOverMenu = GameOverMenu()
        
    def draw(self):
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        if global_vars.GAME_STATE == GAME_STATES["MAINMENU"]:
            self.mainMenu.draw()
        elif global_vars.GAME_STATE == GAME_STATES["HELP"]:
            self.helpMenu.draw()
        elif global_vars.GAME_STATE == GAME_STATES["SELECT WORLD"]:
            self.roomMenu.draw()
        elif global_vars.GAME_STATE == GAME_STATES["ESCAPED"]:
            self.escapeMenu.draw()
        elif global_vars.GAME_STATE == GAME_STATES["GAMEOVER"]:
            self.gameOverMenu.draw()
        elif global_vars.GAME_STATE == GAME_STATES["CREDITS"]:
            self.creditsMenu.draw()
        else:
            print(global_vars.GAME_STATE)
    
    def mouseListener(self, button, state, x, y):
        if global_vars.GAME_STATE == GAME_STATES["MAINMENU"]:
            self.mainMenu.mouseListener(button, state, x, y)
        elif global_vars.GAME_STATE == GAME_STATES["HELP"]:
            self.helpMenu.mouseListener(button, state, x, y)
        elif global_vars.GAME_STATE == GAME_STATES["SELECT WORLD"]:
            self.roomMenu.mouseListener(button, state, x, y)
        elif global_vars.GAME_STATE == GAME_STATES["ESCAPED"]:
            self.escapeMenu.mouseListener(button, state, x, y)
        elif global_vars.GAME_STATE == GAME_STATES["GAMEOVER"]:
            self.gameOverMenu.mouseListener(button, state, x, y)
        elif global_vars.GAME_STATE == GAME_STATES["CREDITS"]:
            self.creditsMenu.mouseListener(button, state, x, y)