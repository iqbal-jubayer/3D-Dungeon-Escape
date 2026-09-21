import os
os.environ["PYOPENGL_PLATFORM"] = "glx"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random

import pygame

WINDOW_SIZE = (720, 520)
GAME_TITLE = "3D Dungeon Escape"
WINDOW_TITLE = b"3D Dungeon Escape"
FPS = 60
fovY = 120  # Field of view

pygame.init()
pygame.mixer.init()

GAME_STATES = {
    "MAINMENU" : 0,
    "SELECT WORLD": 1,
    "GAME" : 2,
    "HELP" : 3,
    "ESCAPED" : 4,
    "GAMEOVER": 5,
    "CREDITS" : 6
}

class GLOBAL_VARS:
    GAME_STATE = GAME_STATES["GAME"]
    VIEW_MODE = 1
    SELECTED_WORLD = 1
    SECONDS = 0
    CHEAT_MODE = False
    ROOM_LEVEL = 1
    PAUSE = False
    dt = 1
    
    room_list = []
    item_list = []
    trap_list = []
    static_item_list = []
    hint_arrow_list = []
    enemy_list = []
    
    player = None
    hud = None
    level = None
    
    DRAWING_RADIUS = 1000
    
    
    enemy_sound_channel = pygame.mixer.Channel(1)
    enemy_sound_timer = 0
    enemy_sound_list = [
        pygame.mixer.Sound("audio/Ghost.mp3"),
        pygame.mixer.Sound("audio/zombie.mp3")
    ]
    enemy_sound_last = None
    enemy_sound_time_delay = 3

global_vars = GLOBAL_VARS()

# Utility Functions
def getDistance(obj1_x, obj1_y, obj2_x, obj2_y):
    distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
    return distance

def convert_coordinate(x, y, window_width, window_height):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (window_width / 2)
    b = (window_height / 2) - y
    return a, b

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1,1,1)):
    r, g, b = color
    glColor4f(r, g, b, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    # gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    gluOrtho2D(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2)

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_rect(x, y, width, height, color=(1,1,1), color1=None, color2=None,color3=None):
    if color1 is None:
        color1 = color
        
    if color2 is None:
        color2 = color
        
    if color3 is None:
        color3 = color
        
    r, g, b = color
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r3, g3, b3 = color3
    glBegin(GL_QUADS)
    
    glColor4f(r, g, b, 1)
    glVertex3f(x+width//2, y-height//2, 0)
    
    glColor4f(r1, g1, b1, 1)
    glVertex3f(x-width//2, y-height//2, 0)
    
    glColor4f(r2, g2, b2, 1)
    glVertex3f(x-width//2, y+height//2, 0)
    
    glColor4f(r3, g3, b3, 1)
    glVertex3f(x+width//2, y+height//2, 0)
    glEnd()

def setup_projection():
    glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def updateLevel():
    global_vars.ROOM_LEVEL += 1
    

# Utility Classes
class BUTTON:
    def __init__(self,x,y,width,height,color=(1,1,1),text="Button"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        
    def draw(self):
        draw_rect(self.x, self.y, self.width, self.height, color=self.color)
        draw_text(self.x-5*len(self.text), self.y, self.text, color=(0,0,0))
        
    def click(self, mouseX, mouseY, callback=None, *args):
        if self.x - self.width//2 < mouseX < self.x + self.width//2 and self.y - self.height//2 < mouseY < self.y + self.height//2:
            if callback is not None:
                callback(*args)
