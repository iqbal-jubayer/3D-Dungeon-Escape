# Name: Jubayer Iqbal
# ID: 24101512

import os
os.environ["PYOPENGL_PLATFORM"] = "glx"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

WINDOW_SIZE = (720, 520)
WINDOW_TITLE = b"3D Dungeon Escape"
FPS = 60
fovY = 120  # Field of view

# GAME CONSTANTS
FIRST_PERSON = True

# GAME_STATE
#   - MENU
#   - HELP
#   - GAME
#   - ESCAPED
GAME_STATE = "GAME"

FLOOR_COLOR = (0.30, 0.25, 0.20)
WALL_COLOR = (0.20, 0.23, 0.28)

KEY_W = False
KEY_A = False
KEY_S = False
KEY_D = False

# classes
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
        
    def click(self, mouseX, mouseY, callback=None):
        if self.x - self.width//2 < mouseX < self.x + self.width//2 and self.y - self.height//2 < mouseY < self.y + self.height//2:
            if callback is not None:
                callback()

class CAMERA:
    camera_x = 0
    camera_y = 0
    camera_z = 0

    target_x = 0
    target_y = 0
    target_z = 0
    
    target_up = 0

    def __init__(self):
        self.distance = 40

    def update(self):
        theta = math.radians(player.angle)
        fx = math.sin(theta)
        fy = -math.cos(theta)
        
        if not FIRST_PERSON:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            
            self.camera_x = player.x
            self.camera_y = player.y + self.distance
            self.camera_z = 500
            
            self.target_x = player.x
            self.target_y = player.y
            self.target_z = 0
            return
        
        self.camera_x = player.x - fx * self.distance
        self.camera_y = player.y - fy * self.distance
        self.camera_z = (player.z - player.height//2) + player.height * 1.2
        
        self.target_x = player.x + fx * self.distance
        self.target_y = player.y + fy * self.distance
        self.target_z = (player.z - player.height) + player.height * 1

class WALL:
    def __init__(self, x, y, width, height, depth, col_x, col_y, color=(1,1,1), orientaion=0):
            # orientaion-
            #   0. Vertical
            #   1. Horizontal
            self.x = x
            self.y = y
            self.z = height//2 * depth + depth//2
            self.width = width
            self.height = height
            self.depth = depth
            self.col_x = col_x
            self.col_y = col_y
            self.color = color
            self.orientaion = orientaion
            
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
        if self.orientaion == 0:
            glScalef(self.depth, self.width * self.depth, self.height * self.depth)
        else:
            glScalef(self.width * self.depth, self.depth, self.height * self.depth)
        glutSolidCube(1)
        glPopMatrix()
        
    def collision_detection(self, x, y, radius):
        if self.orientaion == 0:
            min_x = (self.x + self.col_x) - self.depth//2
            max_x = (self.x + self.col_x) + self.depth//2
            
            min_y = (self.y + self.col_y) - (self.width * self.depth)/2
            max_y = (self.y + self.col_y) + (self.width * self.depth)/2
        else:
            min_x = (self.x + self.col_x) - (self.width * self.depth)/2
            max_x = (self.x + self.col_x) + (self.width * self.depth)/2
            
            min_y = (self.y + self.col_y) - self.depth//2
            max_y = (self.y + self.col_y) + self.depth//2
        
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)
   
class WALL_VERTICAL(WALL):
    def __init__(self, x, y, width, height, depth, col_x, col_y, color=(1,1,1)):
        super().__init__(x, y, width, height, depth, col_x, col_y, color, 0)
        
class WALL_HORIZONTAL(WALL):
    def __init__(self, x, y, width, height, depth, col_x, col_y, color=(1,1,1)):
            super().__init__(x, y, width, height, depth, col_x, col_y, color, 1)

class ROOM:
    def __init__(self, x, y, width, length, tile_size=50, floor_color=(0.30, 0.25, 0.20)):
        self.x = x
        self.y = y
        self.z = 0
        self.width = width
        self.length = length
        self.tile_size = tile_size
        
        self.walls = []
        self.floor_color = floor_color
        
        if self.width % 2 != 0:
            self.width += 1
        if self.length % 2 != 0:
            self.length += 1
            
    def player_light_up(self, rect_x, rect_y):
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
        return r, g, b
        
    def draw_floor(self):
        for j in range(-self.length//2, self.length//2 + 1, 1):
            for i in range(-self.width//2, self.width//2 + 1, 1):
                rect_x = i*(self.tile_size + 0)
                rect_y = j*(self.tile_size + 0)
                
                r, g, b = self.player_light_up(rect_x, rect_y)
                    
                for item in static_item_list:
                    dst = math.sqrt((rect_x + self.x - item.x)**2 + (rect_y + self.y - item.y)**2)
                    if dst < 50:
                        r += 0.35
                        g += 0.25
                        b += 0.10
    
                    elif dst < 100:
                        r += 0.20
                        g += 0.13
                        b += 0.05
    
                    elif dst < 150:
                        r += 0.08
                        g += 0.05
                        b += 0.02
                        
                for item in item_list:
                    try:
                        if not item.isLightSource:
                            continue
                        if not item.active:
                            continue
                    except:
                        continue
                    dst = math.sqrt((rect_x + self.x - item.x)**2 + (rect_y + self.y - item.y)**2)
                    if dst < 50:
                        r += 0.35
                        g += 0.25
                        b += 0.10
    
                    elif dst < 80:
                        r += 0.20
                        g += 0.13
                        b += 0.05
    
                    elif dst < 120:
                        r += 0.08
                        g += 0.05
                        b += 0.02
                draw_rect(rect_x, rect_y, self.tile_size, self.tile_size, color=(r, g, b))
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        self.draw_floor()
        for obj in self.walls:
            obj.draw()
        glPopMatrix()
        
    def collision_detection(self, x, y, radius):
        for obj in self.walls:
            if obj.collision_detection(x, y, radius):
                return True
        return False

    def keyboard_listener(self, key):
        for obj in self.walls:
            try:
                obj.keyboard_listener(key)
            except:
                pass

class STARTROOM(ROOM):
    def __init__(self, x, y, width, length, tile_size=50, wall_color=(0.20, 0.23, 0.28), floor_color=(0.30, 0.25, 0.20)):
        super().__init__(x, y, width, length, tile_size, floor_color)
        self.walls.append(WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        self.walls.append(WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        self.walls.append(WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, 16, 3, 50, self.x, self.y, color=wall_color))
        self.walls.append(WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width, 3, 50, self.x, self.y, color=wall_color))
        
class TUNNEL(ROOM):
    def __init__(self, x, y, width, length, tile_size=50, type="VERTICAL", wall_color=(0.20, 0.23, 0.28), floor_color=(0.30, 0.25, 0.20)):
        super().__init__(x, y, width, length, tile_size, floor_color)
        # TOP - self.walls.append(WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color))
        # BOTTOM - self.walls.append(WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color))
        # RIGHT - self.walls.append(WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        # LEFT - self.walls.append(WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color))
        RIGHT = WALL_VERTICAL(self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color)
        LEFT = WALL_VERTICAL(-self.width//2 * self.tile_size, 0, self.length + 1, 3, 50, self.x, self.y, color=wall_color)
        TOP = WALL_HORIZONTAL(0, -self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color)
        BOTTOM = WALL_HORIZONTAL(0, self.length//2 * self.tile_size, self.width + 1, 3, 50, self.x, self.y, color=wall_color)
        if type == "VERTICAL":
            self.walls.append(RIGHT)
            self.walls.append(LEFT)
        elif type == "HORIZONTAL":
            self.walls.append(TOP)
            self.walls.append(BOTTOM)
        elif type=="TOP_LEFT":
            self.walls.append(TOP)
            self.walls.append(RIGHT)
        elif type=="TOP_RIGHT":
            self.walls.append(TOP)
            self.walls.append(LEFT)
        elif type=="BOTTOM_LEFT":
            self.walls.append(BOTTOM)
            self.walls.append(RIGHT)
        elif type=="BOTTOM_RIGHT":
            self.walls.append(BOTTOM)
            self.walls.append(LEFT)
        elif type=="BOTTOM_LEFT_RIGHT":
            self.walls.append(BOTTOM)
            self.walls.append(RIGHT)
            self.walls.append(LEFT)
        elif type=="TOP_LEFT_RIGHT":
            self.walls.append(TOP)
            self.walls.append(RIGHT)
            self.walls.append(LEFT)

class Player:
    x = 0
    y = 0
    z = 0
    
    health = 100
    max_health = 100
    
    shield = 100
    max_shield = 100
    
    speed = 0
    acc = 3
    
    rot_acc = 5
    angle = 0
    
    keys = []
    
    leg_angle = 0
    leg_angle_dir = 1
    leg_angle_limit = 20
    
    armor_on = True
    
    speedZ = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.width = 30
        self.depth = 10
        self.height = 80
        self.z = self.height//2
        self.rooms = []
        self.keys = []
    
    b = True
    a = True
    t = 5
    t_max = 2
    
    def draw(self):
        glColor3f(1, 0, 0)
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        
        # if self.b:
        #     if self.a:
        #         glTranslatef(-1, 0, 0)
        #     else:
        #         glTranslatef(1, 0, 0)
        #     if self.t <= 0:
        #         self.a = not self.a
        #         self.t = self.t_max
        #     self.t -= 1
        #     self.b = False
        
        glPushMatrix()
        
        # Head
        glPushMatrix()
        glColor3f(0.72, 0.45, 0.25)
        glTranslatef(0, 0, self.height//2 - self.height*0.1)
        glScalef(self.width*0.5, self.width*0.5, 0.2 * self.height)
        glutSolidCube(1)
        glPopMatrix()
        
        if self.armor_on:
            # Halmet
            glPushMatrix()
            glColor3f(0.10, 0.65, 0.75)
            glTranslatef(0, 0, self.height*(0.5-0.05))
            glScalef(self.width*0.6, self.width*0.6, self.height*0.12)
            glutSolidCube(1)
            glPopMatrix()
        
        
        # Body
        glPushMatrix()
        glColor3f(0.25, 0.35, 0.12)
        if self.armor_on:
            glColor3f(0.08, 0.55, 0.65)
        glTranslatef(0, 0, self.height*0.5 - self.height*0.45)
        glScalef(self.width, self.depth, self.height*0.5)
        glutSolidCube(1)
        glPopMatrix()
        
        
        # Right Leggings
        glPushMatrix()
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.3)
        glRotatef(self.leg_angle, 1, 0, 0)
        glTranslatef(0, 0, -(-self.height*0.5 + self.height*0.3))
        # Right Leg
        glPushMatrix()
        glColor3f(0.20, 0.12, 0.07)
        if self.armor_on:
            glColor3f(0.06, 0.42, 0.50)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.15)
        glTranslatef(-self.width*0.25, 0, 0)
        glScalef(self.width*0.4, self.depth, self.height*0.3)
        glutSolidCube(1)
        glPopMatrix()
        
        # Right Boot
        glPushMatrix()
        glColor3f(0.12, 0.07, 0.04)
        if self.armor_on:
            glColor3f(0.05, 0.35, 0.42)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.05)
        glTranslatef(-self.width*0.25, 0, 0)
        glScalef(self.width//2, self.depth+1, self.height*0.1)
        glutSolidCube(1)
        glPopMatrix()
        glPopMatrix()
        
        
        # Left Leggings
        glPushMatrix()
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.3)
        glRotatef(self.leg_angle, -1, 0, 0)
        # Left Leg - upper
        glTranslatef(0, 0, -(-self.height*0.5 + self.height*0.3))
        glPushMatrix()
        glColor3f(0.20, 0.12, 0.07)
        if self.armor_on:
            glColor3f(0.06, 0.42, 0.50)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.15)
        glTranslatef(self.width*0.25, 0, 0)
        glScalef(self.width*0.4, self.depth, self.height*0.3)
        glutSolidCube(1)
        glScalef(1/(self.width*0.4), 1/self.depth, 1/(self.height*0.3))
        glPopMatrix()
        
        # Left Boot
        glPushMatrix()
        glColor3f(0.12, 0.07, 0.04)
        if self.armor_on:
            glColor3f(0.05, 0.35, 0.42)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.05)
        glTranslatef(self.width*0.25, 0, 0)
        glScalef(self.width//2, self.depth+1, self.height*0.1)
        glutSolidCube(1)
        glPopMatrix()
        glPopMatrix()
        
        
        # Left Hand
        glPushMatrix()
        glTranslatef(self.width*0.6, 0, self.height*0.3 - self.height*0.1)
        glRotate(self.leg_angle, 1, 0, 0)
        glTranslatef(-self.width*0.6, 0, -(self.height*0.3 - self.height*0.1))
        
        # Left Arm
        glPushMatrix()
        glColor3f(0.72, 0.45, 0.25)
        glTranslatef(self.width*0.6, 0, self.height*0.1)
        glScalef(self.width*0.2, self.depth, self.height*0.4)
        glutSolidCube(1)
        glPopMatrix()
        
        # Left Shoulder
        glPushMatrix()
        glColor3f(0.25, 0.35, 0.12)
        if self.armor_on:
            glColor3f(0.07, 0.45, 0.52)
        glTranslatef(self.width*0.6, 0, self.height*0.3 - self.height*0.1)
        glScalef(self.width*0.2+1, self.depth+1, self.height*0.2+1)
        glutSolidCube(1)
        glPopMatrix()
        glPopMatrix()
        
        # Right Hand
        glPushMatrix()
        glTranslatef(self.width*0.6, 0, self.height*0.3 - self.height*0.1)
        glRotate(self.leg_angle, -1, 0, 0)
        glTranslatef(-self.width*0.6, 0, -(self.height*0.3 - self.height*0.1))
        
        # Right Arm
        glPushMatrix()
        glColor3f(0.72, 0.45, 0.25)
        glTranslatef(-self.width*0.6, 0, self.height*0.1)
        glScalef(self.width*0.2, self.depth, self.height*0.4)
        glutSolidCube(1)
        glPopMatrix()
        
        # Right Shoulder
        glPushMatrix()
        glColor3f(0.25, 0.35, 0.12)
        if self.armor_on:
            glColor3f(0.07, 0.45, 0.52)
        glTranslatef(-self.width*0.6, 0, self.height*0.3 - self.height*0.1)
        glScalef(self.width*0.2+1, self.depth+1, self.height*0.2+1)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        glPopMatrix()
        
    def move_leg(self):
        self.leg_angle += 1 * self.leg_angle_dir
        if self.leg_angle > self.leg_angle_limit:
            self.leg_angle = self.leg_angle_limit
            self.leg_angle_dir *= -1
        if self.leg_angle < -self.leg_angle_limit:
            self.leg_angle = -self.leg_angle_limit
            self.leg_angle_dir *= -1
    
    def damage(self, point):
        self.b = True
        if self.armor_on:
            self.shield -= point*1.5
            if self.shield <= 0:
                self.armor_on = False
        else:
            self.health -= point
      
    def update(self):
        if KEY_W:
            self.speed += 3
        if KEY_S:
            self.speed -= 3
        
        theta = math.radians(self.angle)
        dx = math.sin(theta) * self.speed
        dy = -math.cos(theta) * self.speed
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        move_x = True
        move_y = True
        for room in room_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 30))
            move_y = (move_y and not room.collision_detection(self.x, new_y, 30))
        
        for item in item_list:
            move_x = (move_x and not item.collision_detection(new_x, self.y, 30))
            move_y = (move_y and not item.collision_detection(self.x, new_y, 30))
        
        if abs(self.x - new_x) > 0.1 or abs(self.y - new_y) > 0.1:
            self.move_leg()
        else:
            self.leg_angle = 0
            
        if move_x:
            self.x = new_x
            
        if move_y:
            self.y = new_y
            
        self.speed *= 0.5
        
        self.z += self.speedZ
        self.speedZ -= 0.5

        if self.z <= self.height // 2:
            self.z = self.height // 2
            self.speedZ = 0

class STATIC_OBJECT:
    def __init__(self, x, y, z, width, height, depth, isLightSource=False):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.isLightSource = isLightSource
        
    def draw(self):
        pass
        
    def update(self):
        pass
    
class TORCH(STATIC_OBJECT):
    def __init__(self, x, y, z, width, height, depth):
        super().__init__(x, y, z, width, height, depth, isLightSource=True)
        
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)
        
        glColor3f(0.25, 0.10, 0.03)
        glTranslatef(0, 0, -0.1*self.height)
        glScale(self.width, self.depth, 0.8*self.height)
        glutSolidCube(1)
        glScale(1/self.width, 1/self.depth, 1/(0.8*self.height))
        
        glColor3f(1, 1, 0)
        glTranslatef(0, 0, 0.5*self.height)
        glScale(self.width, self.depth, 0.2*self.height)
        glutSolidCube(1)
        
        glPopMatrix()

class DOOR:
    def __init__(self, x, y, z, width, height, required_key_name=None):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = 5
        self.required_key_name = required_key_name
        self.locked = True
        if self.required_key_name is None:
            self.locked = False
        
        self.angle = 0
        self.closed = True
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        
        glTranslatef(-self.width/2, 0, 0)
        glRotate(self.angle, 0, 0, -1)
        glTranslatef(self.width/2, 0, 0)
        glColor3f(0.25, 0.10, 0.03)
        # glColor4f(0.25, 0.10, 0.03, 0.8)
        glScalef(self.width, 5, self.height)
        glutSolidCube(1)
        glScalef(1/self.width, 1/5, 1/self.height)
        glTranslatef(self.width/2 - 6, 0, 0)
        glColor3f(1, 1, 0)
        glutSolidCube(6)
        glPopMatrix()
        
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.width:
            if self.locked:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "[LOCKED]")
            else:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "Press \'Space\'")
    
    def update(self):
        if self.closed:
            if self.angle > 0:
                self.angle -= 5
        else:
            if self.angle < 90:
                self.angle += 5
        
    def keyboard_listener(self, key):
        if key == b' ':
            distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
            if distance < self.width:
                if not self.locked:
                    self.closed = not self.closed
                elif any(name==self.required_key_name for name, color in player.keys):
                    self.locked = False
                    self.closed = not self.closed
                
    def collision_detection(self, x, y, radius):
        if not self.closed:
            return False
        min_x = self.x - self.width/2
        max_x = self.x + self.width/2
        
        min_y = self.y - self.depth//2
        max_y = self.y + self.depth//2
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)

class ESCAPE_DOOR(DOOR):
    def __init__(self, x, y, z, width, height, required_key_name=None):
        super().__init__(x, y, z, width, height, required_key_name)
        self.over = False
        self.t = 0
        
    def update(self):
        global GAME_STATE
        super().update()
        if not self.closed:
            self.over = True
        if self.over:
            if self.t < 100:
                self.t += 1
            else:
                GAME_STATE = 'ESCAPED'
                self.over = False

class ITEM:
    def __init__(self, x, y, z, width, height, depth, radius, color, visible=True, active=True, callback=None, rotation=0, isLightSource=False):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.radius = radius
        self.color = color
        self.visible = visible
        self.active = active
        self.callback = callback
        self.rotation = rotation
        self.isLightSource = isLightSource
        
    def draw(self):
        pass

class KEY(ITEM):
    def __init__(self, x, y, z, width, height, depth, radius, color, visible=True, active=True, callback=None, rotation=0, name="KEY_X"):
        super().__init__(x, y, z, width, height, depth, radius, color, visible, active, callback, rotation, isLightSource=True)
        self.solid = False
        self.name = name
    
    def draw(self):
        if not self.visible:
            return
        r, g, b = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, 30)
        glRotatef(self.rotation, 0, 0, 1)
        
        glColor(r, g, b)
        glScalef(40, 3, 3)
        glutSolidCube(1)
        glScalef(1/40, 1/3, 1/3)
        
        glTranslatef(17, 0, -5)
        glScalef(3, 3, 10)
        glutSolidCube(1)
        glScalef(1/3, 1/3, 1/10)
        
        glTranslatef(-10, 0, 0)
        glScalef(3, 3, 10)
        glutSolidCube(1)
        glScalef(1/3, 1/3, 1/10)
        
        glTranslatef(-30, 0, 5)
        gluSphere(gluNewQuadric(), 8, 10, 10)
        
        glPopMatrix()

    def collision_detection(self, x, y, radius):
        if not self.active:
            return
        min_x = self.x - self.radius
        max_x = self.x + self.radius
        
        min_y = self.y - self.radius
        max_y = self.y + self.radius
        if (x + radius > min_x and x - radius < max_x and y + radius > min_y and y - radius < max_y):
            try:
                self.callBack()
            except:
                pass

    def keyboard_listener(self, key):
        pass
        
    def update(self):
        self.rotation += 1

    def callBack(self):
        self.visible = False
        self.active = False
        player.keys.append((self.name, self.color))

class HUD:
    def __init__(self):
        pass
    
    def draw_key_hud(self):
        draw_text(-WINDOW_SIZE[0]//2 + 10, WINDOW_SIZE[1]//2 - 100 - 20, "KEYS: ")
        for i in range(len(player.keys)):
            x = -WINDOW_SIZE[0]//2 + 90 + i*45
            y = WINDOW_SIZE[1]//2 - 92 - 20
            draw_rect(x, y, 30, 5, color=player.keys[i][1])
            draw_rect(x-12.5, y-5, 5, 10, color=player.keys[i][1])
            draw_rect(x-5, y-5, 5, 10, color=player.keys[i][1])
            draw_rect(x + 15, y, 10, 10, color=player.keys[i][1])
            
    def draw_player_health(self):
        draw_text(-350, 205, "Player")
        bar_color = (0, 1, 0)
        if player.health < 20:
            bar_color = (1, 0, 0)
        elif player.health < 50:
            bar_color = (1, 1, 0)
        draw_rect(-275 - (150 - (150 * (player.health/100)))//2, 210, 150 * (player.health/100), 20, bar_color)
        
    def draw_player_shield(self):
        if not player.armor_on:
            return
        draw_text(-350, 180, "Shield")
        bar_color = (0.10, 0.65, 0.75)
        draw_rect(-275 - (150 - (150 * (player.shield/100)))//2, 185, 150 * (player.shield/100), 20, bar_color)
    
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
            
            
        # Restore original projection and modelview matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def update(self):
        pass

class SPIKETRAP:
    def __init__(self, x, y, z, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.damage = 20
            
    def draw(self):
        glPushMatrix()
        glColor3f(0.18, 0.16, 0.14)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.width, self.width, 1)
        glutSolidCube(1)
        glScalef(1/self.width, 1/self.width, 1)
        
        glColor3f(0.32, 0.35, 0.38)
        glTranslatef(self.width/2 - 6, -self.width//2 + 8, 0)
        for j in range(4):
            for i in range(4):
                gluCylinder(gluNewQuadric(), self.width/10, 0, 30, 10, 10)
                glTranslatef(-self.width/4, 0, 0)
            glTranslatef(self.width, self.width/4, 0)
            
        glTranslatef(0, -self.width, 18)
        
        glColor3f(0.55, 0.58, 0.62)
        for j in range(4):
            for i in range(4):
                gluCylinder(gluNewQuadric(), self.width/20, 0, 12, 10, 10)
                glTranslatef(-self.width/4, 0, 0)
            glTranslatef(self.width, self.width/4, 0)
        
        glPopMatrix()
    
    def update(self):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.width//2 + player.width//2 and player.z - player.height//2 < self.height:
            player.damage(self.damage)
            player.speed -= 20

class POISONTRAP:
    def __init__(self, x, y, z, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.damage = 0.05
            
    def draw(self):
        glPushMatrix()
        glColor3f(0.45, 0.10, 0.55)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.width, self.width, 1)
        glutSolidCube(1)
        glScalef(1/self.width, 1/self.width, 1)
        
        glColor3f(0.40, 0.75, 0.05)
        glTranslatef(self.width/2 - 6, -self.width//2 + 8, 0)
        for j in range(4):
            for i in range(4):
                glutSolidCube(2)
                glTranslatef(-self.width/4, 0, 0)
            glTranslatef(self.width, self.width/4, 0)
        
        glPopMatrix()
    
    def update(self):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.width//2 + player.width//2 and player.z - player.height//2 < self.height:
            player.damage(self.damage)
            # player.speed -= 20

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

# DEBUGING
class DEBUG:
    text_x = 0
    text_y = 0
    tick = 0

debug = DEBUG()

# Callbacks
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    
    global FIRST_PERSON, KEY_W, KEY_S, text_x, text_y, GAME_STATE
    if GAME_STATE == "GAME":
        if key == b'w':
            # player.speed += 10
            KEY_W = True
        if key == b's':
            # player.speed -= 10
            KEY_S = True
        if key == b'a':
            player.angle += 20
        if key == b'd':
            player.angle -= 20
        
        if key == b'u':
            room_to_move.y -= 10
            debug.text_y += 50
        if key == b'j':
            room_to_move.y += 10
            debug.text_y -= 50
        if key == b'h':
            room_to_move.x += 10
            debug.text_x -= 50
        if key == b'k':
            room_to_move.x -= 10
            debug.text_x += 50
            
        if key == b'z':
            player.armor_on = not player.armor_on
            
        if key == b'v':
            FIRST_PERSON = not FIRST_PERSON
            
        if key == b' ':
            # player.armor_on = not player.armor_on
            # print(room_to_move.x, room_to_move.y)
            # print(debug.text_x, debug.text_y)
            player.speedZ = 8
            pass
            
        for room in room_list:
            room.keyboard_listener(key)
        
        for item in item_list:
            item.keyboard_listener(key)

    if key == b'\x1b':
        # GAME_STATE = "MENU"
        glutLeaveMainLoop()

# SHOULD BE REMOVED
def keyboardUpListener(key, x, y):
    global KEY_W, KEY_S
    if key == b'w':
        KEY_W = False
    if key == b's':
        KEY_S = False

def specialKeyListener(key, x, y):
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        camera.target_up += 5
        
    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        camera.target_up -= 5
        
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        pass

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        pass

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
        pass

    elif GAME_STATE == "ESCAPED":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            main_menu_button.click(x, y, main_menu_button_callback)

def idle(value=0):
    
    if GAME_STATE == 'GAME':
        player.update()
        camera.update()
        hud.update()
        for item in item_list:
            item.update()
        for trap in trap_list:
            trap.update()
        
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
    game_init()
help_button =  BUTTON(0, 40, 500, 50, text="HELP")
def help_button_callback():
    global GAME_STATE
    GAME_STATE = "HELP"
help_back_button =  BUTTON(-WINDOW_SIZE[0]//2 + 40, WINDOW_SIZE[1]//2 - 100, 100, 30, text="Back")
def help_back_button_callback():
    global GAME_STATE
    GAME_STATE = "MENU"
exit_button =  BUTTON(0, -20, 500, 50, text="EXIT")
main_menu_button =  BUTTON(0, 40, 500, 50, text="MAINMENU")
def main_menu_button_callback():
    global GAME_STATE
    GAME_STATE = "MENU"

# Creating Objects
camera = CAMERA()

room_list = []
item_list = []
static_item_list = []
enemy_list = []
trap_list = []

room_to_move = None

player = None
hud = None

def game_init():
    global item_list, static_item_list, room_list, room_to_move, player, hud, enemy_list, trap_list
    
    room_list = []
    start_room = STARTROOM(0, 0, 20, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_1 = TUNNEL(350, -500, 6, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_2 = TUNNEL(-350, -500, 6, 10, wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_3 = TUNNEL(-450, -1050, 10, 10, type="TOP_LEFT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_4 = TUNNEL(-750, -1050, 10, 10, type="HORIZONTAL", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_5 = TUNNEL(-1300, -1050, 10, 10, type="TOP_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_6 = TUNNEL(-1300, -550, 10, 10, type="BOTTOM_LEFT_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)
    tunnel_7 = TUNNEL(350, -1035, 6, 10, type="TOP_LEFT_RIGHT", wall_color=WALL_COLOR, floor_color=FLOOR_COLOR)

    room_list.append(start_room)
    room_list.append(tunnel_1)
    room_list.append(tunnel_2)
    room_list.append(tunnel_3)
    room_list.append(tunnel_4)
    room_list.append(tunnel_5)
    room_list.append(tunnel_6)
    room_list.append(tunnel_7)
    
    item_list = []
    door_a = DOOR(439, -245, 50, 75, 100, required_key_name=None)
    key_a = KEY(-1369, -480, 50, 20, 20, 20, 5, color=(1, 1, 0), name="KEY_A")
    escape_door = ESCAPE_DOOR(350, -1260, 100, 100, 200, required_key_name="KEY_A")
    
    item_list.append(door_a)
    item_list.append(key_a)
    item_list.append(escape_door)
    
    static_item_list = []
    torch = TORCH(-240, -1250, 50, 20, 100, 20)
    static_item_list.append(torch)
    
    for i in range(9):
        trap_list.append(SPIKETRAP(-1500 + i * 50, -650, 0, 50, 30))
        
    trap_list.append(POISONTRAP(0, -100, 0, 50, 1))
    
    player = Player(0, 0)
    hud = HUD()
    
    room_to_move = escape_door

game_init()
 
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
    
    draw_text(0, WINDOW_SIZE[1]//2 - 100, "HELP", font=GLUT_BITMAP_TIMES_ROMAN_24)
    help_back_button.draw()

def draw_game():
    for room in room_list:
        room.draw()
        
    for item in item_list:
        item.draw()
        
    for item in static_item_list:
        item.draw()
        
    for trap in trap_list:
        trap.draw()
        
    player.draw()
    hud.draw()

def draw_escaped():
    glColor3f(1, 0, 0)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    end_quote = "A NEW LIFE BEGINS"
    draw_text(-6*len(end_quote), 100, end_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
    main_menu_button.draw()

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
        setupCamera()
        draw_game()
    elif GAME_STATE == "ESCAPED":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_escaped()
        
    
    glutSwapBuffers()

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(WINDOW_SIZE[0], WINDOW_SIZE[1])  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(WINDOW_TITLE)  # Create the window

    # glEnable(GL_BLEND)
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutTimerFunc(1000//FPS, idle, 0)

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
