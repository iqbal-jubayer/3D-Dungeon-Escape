# Name: Jubayer Iqbal
# ID: 24101512

import os

os.environ["PYOPENGL_PLATFORM"] = "glx"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0,-500,400)

fovY = 120  # Field of view

WINDOW_SIZE = (1000,800)
WINDOW_TITLE = b"3D Dungeon Escape"
FPS = 60
FIRST_PERSON = False

# GAME_STATE
#   - MENU
#   - HELP
#   - GAME
GAME_STATE = "MENU"

# classes
class CAMERA:
    camera_x = 0
    camera_y = 0
    camera_z = 0

    target_x = 0
    target_y = 0
    target_z = 0

    def __init__(self):
        self.distance = 80

    def update(self):
        if not FIRST_PERSON:
            self.camera_x = player.x
            self.camera_y = player.y + 100
            self.camera_z = 1000
            
            self.target_x = player.x
            self.target_y = player.y
            self.target_z = 0
            return
        theta = math.radians(player.angle)
        fx = math.sin(theta)
        fy = -math.cos(theta)
        
        self.camera_x = player.x - fx * self.distance
        self.camera_y = player.y - fy * self.distance
        self.camera_z = 100
        
        self.target_x = player.x
        self.target_y = player.y
        self.target_z = 90

class BULB:
    def __init__(self, x, y, z=0, solid=True):
        self.x = x
        self.y = y
        self.z = z
        self.radius = 20
        self.color = (1, 1, 0)
        self.solid = solid
        
    def draw(self):
        r, g, b = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(r, g, b)
        gluSphere(gluNewQuadric(), self.radius, 10, 10)
        glPopMatrix()
        
    def collision_detection(self, x, y, radius):
        min_x = self.x - self.radius//2
        max_x = self.x + self.radius//2
        
        min_y = self.y - self.radius//2
        max_y = self.y + self.radius//2
        
        return (x + radius > min_x and
        x - radius < max_x and
        y + radius > min_y and
        y - radius < max_y)
        
class WALL_VERTICAL:
    def __init__(self, x, y, width, height, depth, col_x, col_y, color=(1,1,1), solid=True):
        self.x = x
        self.y = y
        self.z = height//2 * depth + depth//2
        self.width = width
        self.height = height
        self.depth = depth
        self.col_x = col_x
        self.col_y = col_y
        self.color = color
        self.solid = solid
        
    def draw(self):
        glPushMatrix()
        r, g, b = self.color
        distance = math.sqrt((self.x + self.col_x - player.x)**2 + (self.y + self.col_y - player.y)**2)
        if distance < 75:
            r += 0.35
            g += 0.25
            b += 0.10

        elif distance < 150:
            r += 0.20
            g += 0.13
            b += 0.05

        elif distance < 250:
            r += 0.08
            g += 0.05
            b += 0.02
        glColor3f(r, g, b)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.depth, self.width * self.depth, self.height * self.depth)
        glutSolidCube(1)
        glPopMatrix()
    
    def collision_detection(self, x, y, radius):
        min_y = (self.y + self.col_y) - (self.width * self.depth)/2
        max_y = (self.y + self.col_y) + (self.width * self.depth)/2
        
        min_x = (self.x + self.col_x) - self.depth//2
        max_x = (self.x + self.col_x) + self.depth//2
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)
        
class WALL_HORIZONTAL:
    def __init__(self, x, y, width, height, depth, col_x, col_y, color=(1, 1, 1), solid=True):
        self.x = x
        self.y = y
        self.z = height//2 * depth + depth//2
        self.width = width
        self.height = height
        self.depth = depth
        self.col_x = col_x
        self.col_y = col_y
        self.color = color
        self.solid = solid
        
    def draw(self):
        glPushMatrix()
        r, g, b = self.color
        distance = math.sqrt((self.x + self.col_x - player.x)**2 + (self.y + self.col_y - player.y)**2)
        if distance < 75:
            r += 0.35
            g += 0.25
            b += 0.10

        elif distance < 150:
            r += 0.20
            g += 0.13
            b += 0.05

        elif distance < 250:
            r += 0.08
            g += 0.05
            b += 0.02
        glColor3f(r, g, b)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.width * self.depth, self.depth, self.height * self.depth)
        glutSolidCube(1)
        glPopMatrix()
    
    def collision_detection(self, x, y, radius):
        min_x = (self.x + self.col_x) - (self.width * self.depth)/2
        max_x = (self.x + self.col_x) + (self.width * self.depth)/2
        
        min_y = (self.y + self.col_y) - self.depth//2
        max_y = (self.y + self.col_y) + self.depth//2
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)
        
class ROOM:
    def __init__(self, x, y, width, length, tile_size=50, floor_color=(0.30, 0.25, 0.20)):
        self.x = x
        self.y = y
        self.z = 0
        self.width = width
        self.length = length
        self.tile_size = tile_size
        self.objects = []
        self.floor_color = floor_color
        
        if self.width % 2 != 0:
            self.width += 1
        if self.length % 2 != 0:
            self.length += 1
        
    def draw_floor(self):
        for j in range(-self.length//2, self.length//2 + 1, 1):
            for i in range(-self.width//2, self.width//2 + 1, 1):
                rect_x = i*(self.tile_size + 0)
                rect_y = j*(self.tile_size + 0)
                distance = math.sqrt((rect_x + self.x - player.x)**2 + (rect_y + self.y - player.y)**2)
                r, g, b = self.floor_color
                if distance < 75:
                    r += 0.35
                    g += 0.25
                    b += 0.10

                elif distance < 150:
                    r += 0.20
                    g += 0.13
                    b += 0.05

                elif distance < 250:
                    r += 0.08
                    g += 0.05
                    b += 0.02
                draw_rect(rect_x, rect_y, self.tile_size, self.tile_size, color=(r, g, b))
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        self.draw_floor()
        for obj in self.objects:
            obj.draw()
        glPopMatrix()
        
    def collision_detection(self, x, y, radius):
        for obj in self.objects:
            try:
                obj.update()
            except:
                pass
            if obj.solid and obj.collision_detection(x, y, radius):
                return True
        return False

    def keyboard_listener(self, key):
        for obj in self.objects:
            try:
                obj.keyboard_listener(key)
            except:
                pass

FLOOR_COLOR = (0.30, 0.25, 0.20)
WALL_COLOR = (0.20, 0.23, 0.28)
# FLOOR_COLOR = (1, 1, 1)
# WALL_COLOR = (1, 1, 0)

class STARTROOM(ROOM):
    def __init__(self, x, y, width, length, tile_size=50, wall_color=(0.20, 0.23, 0.28), floor_color=(0.30, 0.25, 0.20)):
        super().__init__(x, y, width, length, tile_size, floor_color)
        self.objects.append(WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        self.objects.append(WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        self.objects.append(WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, 7, 3, 50, self.x, self.y, color=wall_color))
        self.objects.append(WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width - 1, 3, 50, self.x, self.y, color=wall_color))
        
        self.objects.append(DOOR(0, -100, 50, 60, 100, self.x, self.y))
        
class TUNNEL(ROOM):
    def __init__(self, x, y, width, length, tile_size=50, type="VERTICAL", wall_color=(0.20, 0.23, 0.28), floor_color=(0.30, 0.25, 0.20)):
        super().__init__(x, y, width, length, tile_size, floor_color)
        # TOP - self.objects.append(WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color))
        # BOTTOM - self.objects.append(WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color))
        # RIGHT - self.objects.append(WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        # LEFT - self.objects.append(WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        RIGHT = WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color)
        LEFT = WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color)
        TOP = WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color)
        BOTTOM = WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color)
        if type == "VERTICAL":
            self.objects.append(RIGHT)
            self.objects.append(LEFT)
        elif type == "HORIZONTAL":
            self.objects.append(TOP)
            self.objects.append(BOTTOM)
        elif type=="TOP_LEFT":
            self.objects.append(TOP)
            self.objects.append(RIGHT)
        elif type=="TOP_RIGHT":
            self.objects.append(TOP)
            self.objects.append(LEFT)
        elif type=="BOTTOM_LEFT":
            self.objects.append(BOTTOM)
            self.objects.append(RIGHT)
        elif type=="BOTTOM_RIGHT":
            self.objects.append(BOTTOM)
            self.objects.append(LEFT)
        elif type=="BOTTOM_LEFT_RIGHT":
            self.objects.append(BOTTOM)
            self.objects.append(RIGHT)
            self.objects.append(LEFT)
        elif type=="TOP_LEFT_RIGHT":
            self.objects.append(TOP)
            self.objects.append(RIGHT)
            self.objects.append(LEFT)

class Player:
    x = 0
    y = 0
    speed = 0
    acc = 3
    rot_acc = 5
    angle = 0
    
    def __init__(self):
        self.rooms = []
        
    def add_room(self,room):
        self.rooms.append(room)
    
    def draw(self):
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(self.x, self.y, 20)
        glRotatef(self.angle, 0, 0, 1)
        glutSolidCube(40)
        glTranslatef(0, 0, 20)
        glutSolidCube(40)
        glPopMatrix()
        
    def update(self):
        theta = math.radians(self.angle)
        dx = math.sin(theta) * self.speed
        dy = -math.cos(theta) * self.speed
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        move_x = True
        move_y = True
        for room in draw_rooms_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 30))
            
        for room in draw_rooms_list:
            move_y = (move_y and not room.collision_detection(self.x, new_y, 30))
        
            
        if move_x:
            self.x = new_x
        if move_y:
            self.y = new_y
            
        # if not (start_room.collision_detection(new_x, self.y, 30) or tunnel_1.collision_detection(new_x, self.y, 30)):
        #     self.x = new_x
        
        # if not (start_room.collision_detection(self.x, new_y, 30) or tunnel_1.collision_detection(self.x, new_y, 30)):
        #     self.y = new_y
            
        # self.x = new_x
        # self.y = new_y
        
        self.speed *= 0.5

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
        draw_text(self.x - len(self.text)*2, self.y, self.text, color=(0,0,0))
        
    def click(self, mouseX, mouseY, callback=None):
        if self.x - self.width//2 < mouseX < self.x + self.width//2 and self.y - self.height//2 < mouseY < self.y + self.height//2:
            if callback is not None:
                callback()

class OBJECT:
    def __init__(self, x, y, width, height):
        pass

class DOOR:
    def __init__(self, x, y, z, width, height, col_x, col_y, solid=True):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.col_x = col_x
        self.col_y = col_y
        self.solid = solid
        self.depth = 5
        
        self.angle = 0
        self.closed = True
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glTranslatef(-self.width/2, 0, 0)
        glRotate(self.angle, 0, 0, -1)
        glTranslatef(self.width/2, 0, 0)
        
        
        glColor3f(0.25, 0.10, 0.03)
        glScalef(self.width, 5, self.height)
        glutSolidCube(1)
        glScalef(1/self.width, 1/5, 1/self.height)
        glTranslatef(self.width/2 - 6, 0, 0)
        glColor3f(1, 1, 0)
        glutSolidCube(6)
        
        glPopMatrix()
        
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < 35:
            draw_text(0, -WINDOW_SIZE[1]//2 + 50, "Press \'Space\'")
        
    def operate(self):
        print("PRESSED")
    
    def update(self):
        if self.closed:
            if self.angle > 0:
                self.angle -= 1
        else:
            if self.angle < 90:
                self.angle += 1
        
    def keyboard_listener(self, key):
        if key == b' ':
            distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            if distance < 35:
                self.closed = not self.closed
                
    def collision_detection(self, x, y, radius):
        if not self.closed:
            return False
        min_x = (self.x + self.col_x) - self.width/2
        max_x = (self.x + self.col_x) + self.width/2
        
        min_y = (self.y + self.col_y) - self.depth//2
        max_y = (self.y + self.col_y) + self.depth//2
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)
    

# glutSolidCube(30)
# gluSphere(gluNewQuadric(), 20, 10, 10)
# gluCylinder(gluNewQuadric(), 8, 3, 30, 10, 10)
# draw_text(10, 730, f"Player Bullet Missed: {player.missed}")

def convert_coordinate(x, y):
    """
    Converts mouse (screen) coordinates to OpenGL (Cartesian) coordinates.
    Top-left of the window is (0,0) in screen space,
    but OpenGL center is (0,0).
    """
    a = x - (WINDOW_SIZE[0] / 2)
    b = (WINDOW_SIZE[1] / 2) - y
    return a, b

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1,1,1)):
    r, g, b = color
    glColor3f(r, g, b)
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

def draw_point(size, x, y, z, color=(1,1,1,1)):
    r, g, b, a = color
    glColor4f(r, g, b, a)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex3f(x, y, z)
    glEnd()
    
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
    
    glColor3f(r, g, b)
    glVertex3f(x+width//2, y-height//2, 0)
    
    glColor3f(r1, g1, b1)
    glVertex3f(x-width//2, y-height//2, 0)
    
    glColor3f(r2, g2, b2)
    glVertex3f(x-width//2, y+height//2, 0)
    
    glColor3f(r3, g3, b3)
    glVertex3f(x+width//2, y+height//2, 0)
    glEnd()

# Callbacks
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    
    global FIRST_PERSON
    
    if key == b'w':
        player.speed += 10
    if key == b's':
        player.speed -= 10
    if key == b'a':
        player.angle += 20
    if key == b'd':
        player.angle -= 20
    
    if key == b'u':
        room_to_move.y -= 5
    if key == b'j':
        room_to_move.y += 5
    if key == b'h':
        room_to_move.x += 5
    if key == b'k':
        room_to_move.x -= 5
        
    if key == b'f':
        FIRST_PERSON = not FIRST_PERSON
        
    if key == b' ':
        # start_room.objects[4].closed = not start_room.objects[4].closed
        print(room_to_move.x, room_to_move.y)
    
    if key == b'\x1b':
        glutLeaveMainLoop()
        
    for room in draw_rooms_list:
        room.keyboard_listener(key)

def specialKeyListener(key, x, y):
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        camera.camera_z -= 5
        
    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        camera.camera_z += 5
        
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        start_room.angle += 1

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        start_room.angle -= 1

def mouseListener(button, state, x, y):
    x, y = convert_coordinate(x, y)
    
    if GAME_STATE == "MENU":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            start_button.click(x, y, start_button_callback)
            help_button.click(x,y,help_button_callback)
            exit_button.click(x,y, glutLeaveMainLoop)
            
    elif GAME_STATE == "HELP":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            help_back_button.click(x, y, help_back_button_callback)
            
    elif GAME_STATE == "GAME":
        # Left mouse button fires a bullet
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            pass

        # Right mouse button toggles camera tracking mode
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            pass

def idle(value=0):
    player.update()
    camera.update()
    glutPostRedisplay()
    glutTimerFunc(1000//FPS, idle, 0)

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, WINDOW_SIZE[0]/WINDOW_SIZE[1], 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    
    # Position the camera and set its orientation
    gluLookAt(
        camera.camera_x,
        camera.camera_y,
        camera.camera_z,  # Camera position
        camera.target_x,
        camera.target_y,
        camera.target_z,  # Look-at target
        0, 0, 1)  # Up vector (z-axis)

def setup_projection():
    glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2, 0, 1)
    glMatrixMode(GL_MODELVIEW)

# Creating Buttons
start_button = BUTTON(0, 100, 500, 50, text="START")
def start_button_callback():
    global GAME_STATE
    GAME_STATE = "GAME"
help_button =  BUTTON(0, 40, 500, 50, text="HELP")
def help_button_callback():
    global GAME_STATE
    GAME_STATE = "HELP"
help_back_button =  BUTTON(-400, 300, 100, 50, text="Back")
def help_back_button_callback():
    global GAME_STATE
    GAME_STATE = "MENU"
exit_button =  BUTTON(0, -20, 500, 50, text="EXIT")

# Creating Objects
camera = CAMERA()
# start_room = STARTROOM()

# corridor = CORRIDOR(0, 0, 500, 500)
draw_rooms_list = []
start_room = STARTROOM(0, 0, 20, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_1 = TUNNEL(350, -500, 6, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_2 = TUNNEL(-350, -500, 6, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_3 = TUNNEL(-450, -1050, 10, 10, type="TOP_LEFT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_4 = TUNNEL(-750, -1050, 10, 10, type="HORIZONTAL", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_5 = TUNNEL(-1300, -1050, 10, 10, type="TOP_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_6 = TUNNEL(-1300, -550, 10, 10, type="BOTTOM_LEFT_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
tunnel_7 = TUNNEL(350, -1035, 6, 10, type="TOP_LEFT_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)

draw_rooms_list.append(start_room)
draw_rooms_list.append(tunnel_1)
draw_rooms_list.append(tunnel_2)
draw_rooms_list.append(tunnel_3)
draw_rooms_list.append(tunnel_4)
draw_rooms_list.append(tunnel_5)
draw_rooms_list.append(tunnel_6)
draw_rooms_list.append(tunnel_7)
room_to_move = start_room


player = Player()

    
def draw_menu():
    glColor3f(1, 0, 0)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(-12*5, 200, "3D Dungeon Escape", font=GLUT_BITMAP_TIMES_ROMAN_24)
    
    start_button.draw()
    help_button.draw()
    exit_button.draw()

def draw_help():
    glColor3f(1, 0, 0)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(-12*5, 300, "HELP", font=GLUT_BITMAP_TIMES_ROMAN_24)
    help_back_button.draw()

def draw_brick(x, y, z, width, height,color=(1,0,0)):
    a = width//2
    
    glPushMatrix()
    r, g, b = color
    glColor3f(r, g, b)
    
    glTranslatef(x, y, z)
    glutSolidCube(a)
    glTranslatef(0, a, 0)
    glutSolidCube(a)
    
    glColor3f(0.4, 0.4, 0.4)
    glTranslatef(0, 0, a)
    glutSolidCube(a-1)
    glTranslatef(0, -a, 0)
    glutSolidCube(a-1)
    glTranslatef(0, -a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, a, 0)
    glutSolidCube(a-1)
    glTranslatef(0, a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, 0, a)
    glutSolidCube(a-1)
    glTranslatef(0, 0, a//2)
    glutSolidCube(a-1)
    
    glPopMatrix()

def draw_game():
    for room in draw_rooms_list:
        room.draw()
    player.draw()
    
def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1])  # Set viewport size
    
    setup_projection()
    
    if GAME_STATE == "MENU":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_menu()
    elif GAME_STATE == "HELP":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_help()
    elif GAME_STATE == "GAME":
        glEnable(GL_DEPTH_TEST)
        setupCamera()  # Configure camera perspective
        draw_game()
        
    
    glutSwapBuffers()

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(WINDOW_SIZE[0], WINDOW_SIZE[1])  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(WINDOW_TITLE)  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutTimerFunc(1000//FPS, idle, 0)

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
