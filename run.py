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
CHEAT_MODE = False

# GAME_STATE
#   - MENU
#   - HELP
#   - GAME
#   - ESCAPED
GAME_STATE = "GAME"

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
        
        if False:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            
            self.camera_x = player.x
            self.camera_y = player.y + self.distance
            self.camera_z = 1000
            
            self.target_x = player.x
            self.target_y = player.y
            self.target_z = 0
            return
        
        if False:
            self.camera_x = player.x + fx * 10
            self.camera_y = player.y - fy * -20
            self.camera_z = (player.z - player.height//2) + player.height
            
            self.target_x = player.x + fx * self.distance
            self.target_y = player.y + fy * self.distance
            self.target_z = (player.z - player.height) + player.height * 1.5
            return
        
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



class UNIT_WALL:
    def __init__(self, x, y, z, width, depth, height, colx, coly, color=(1, 0, 0, 1), orientaion=0):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height
        self.col_x = colx
        self.col_y = coly
        self.color = color
        self.orientaion = orientaion
        
    def draw(self):
        r, g, b, a = self.color
        distance = math.sqrt((self.x + self.col_x - player.x)**2 + (self.y + self.col_y - player.y)**2)
        if distance < 75:
            r += 0.15
            g += 0.10
            b += 0.04

        elif distance < 150:
            r += 0.08
            g += 0.05
            b += 0.02

        elif distance < 250:
            r += 0.03
            g += 0.02
            b += 0.01
        glColor4f(r, g, b, 0.9)
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        scaleX = self.depth
        scaleY = self.width
        if self.orientaion == 1:
            scaleX, scaleY = scaleY, scaleX
        glScalef(scaleX, scaleY, self.height)
        glutSolidCube(1)
        glPopMatrix()
    
    def update(self):
        pass
    
    def collision_detection(self, x, y, radius):
        if self.orientaion == 0:
            min_x = (self.x + self.col_x) - self.depth//2
            max_x = (self.x + self.col_x) + self.depth//2
            
            min_y = (self.y + self.col_y) - self.width//2
            max_y = (self.y + self.col_y) + self.width//2
            
        else:
            min_x = (self.x + self.col_x) - self.width//2
            max_x = (self.x + self.col_x) + self.width//2
            
            min_y = (self.y + self.col_y) - self.depth//2
            max_y = (self.y + self.col_y) + self.depth//2
        
        
        return (x + radius > min_x and
                x - radius < max_x and
                y + radius > min_y and
                y - radius < max_y)
                
def create_vertical_wall(x, y, z, tile_size, n, height, col_x, col_y, color=(1, 0, 0, 1), orientation=0):
    walls = []
    for i in range(n):
        if orientation == 0:
            walls.append(UNIT_WALL(x, y + i*tile_size, height*0.5, 50, 10, height, col_x, col_y, color, orientation))
        else:
            walls.append(UNIT_WALL(x + i*tile_size, y, height*0.5, 50, 10, height, col_x, col_y, color, orientation))
    return walls

class AREA:
    def __init__(self, x, y, width, length, tile_size=50, floor_color=(0.30, 0.25, 0.20, 1)):
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
            
    def floor_light_up(self, rect_x, rect_y, obj_x, obj_y, color):
        r, g, b, a = color
        distance = math.sqrt((rect_x + self.x - obj_x)**2 + (rect_y + self.y - obj_y)**2)
        if distance < 75:
            r += 0.15
            g += 0.10
            b += 0.04

        elif distance < 150:
            r += 0.08
            g += 0.05
            b += 0.02

        elif distance < 250:
            r += 0.03
            g += 0.02
            b += 0.01
        return r, g, b, a
            
    def player_light_up(self, rect_x, rect_y):
        distance = math.sqrt((rect_x + self.x - player.x)**2 + (rect_y + self.y - player.y)**2)
        r, g, b, a = self.floor_color
        if distance < 75:
            r += 0.15
            g += 0.10
            b += 0.04

        elif distance < 150:
            r += 0.08
            g += 0.05
            b += 0.02

        elif distance < 250:
            r += 0.03
            g += 0.02
            b += 0.01
        return r, g, b, a
        
    def draw_floor(self):
        for j in range(-self.length//2, self.length//2, 1):
            for i in range(-self.width//2, self.width//2, 1):
                rect_x = i*(self.tile_size + 0)
                rect_y = j*(self.tile_size + 0)
                r, g, b, a = self.floor_color
                
                r, g, b, a = self.floor_light_up(rect_x, rect_y, player.x, player.y, (r, g, b, a))
                    
                for item in static_item_list:
                    if not item.isLightSource:
                        continue
                    r, g, b, a = self.floor_light_up(rect_x, rect_y, item.x, item.y, (r, g, b, a))
                        
                for item in item_list:
                    try:
                        if not item.isLightSource:
                            continue
                        if not item.active:
                            continue
                    except:
                        continue
                    r, g, b, a = self.floor_light_up(rect_x, rect_y, item.x, item.y, (r, g, b, a))
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

class ROOM(AREA):
    def __init__(self, x, y, width, length, tile_size=50, wall_color=(0.08, 0.10, 0.13, 1), floor_color=(0.12, 0.10, 0.08, 1), door_at="tblf", gap_at=""):
        super().__init__(x, y, width, length, tile_size, floor_color)
        
        wall_height = 100
        
        ts = self.tile_size*0.5
        # Left
        LEFT_WALL = create_vertical_wall((self.width-1)*ts, -self.length*ts, 25, self.tile_size, self.length, wall_height, self.x, self.y, wall_color, 0)
        LEFT_TOP = create_vertical_wall((self.width-1)*ts, -self.length*ts, 25, self.tile_size, int(self.length/2) + (self.length%2), wall_height, self.x, self.y, wall_color, 0)
        LEFT_BOTTOM = create_vertical_wall((self.width-1)*ts, -self.length*ts + (self.length/2+1)*self.tile_size, 25, self.tile_size, int(self.length/2) + (self.length%2-1), wall_height, self.x, self.y, wall_color, 0)
        
        # Right
        RIGHT_WALL = create_vertical_wall(-self.width*ts-20, -self.length*ts, 25, self.tile_size, self.length, wall_height, self.x, self.y, wall_color, 0)
        RIGHT_TOP = create_vertical_wall(-self.width*ts-20, -self.length*ts, 25, self.tile_size, int(self.length/2) + (self.length%2), wall_height, self.x, self.y, wall_color, 0)
        RIGHT_BOTTOM = create_vertical_wall(-self.width*ts-20, -self.length*ts + (self.length/2+1)*self.tile_size, 25, self.tile_size, int(self.length/2) + (self.length%2-1), wall_height, self.x, self.y, wall_color, 0)
        
        
        # Top
        TOP_WALL = create_vertical_wall(-self.width*ts, -self.length*ts-20, 25, self.tile_size, self.width, wall_height, self.x, self.y, wall_color, 1)
        TOP_LEFT = create_vertical_wall(-self.width*ts, -self.length*ts-20, 25, self.tile_size, int(self.width/2) + (self.width%2), wall_height, self.x, self.y, wall_color, 1)
        TOP_RIGHT = create_vertical_wall(-self.width*ts + (self.width/2+1)*self.tile_size, -self.length*ts-20,25,self.tile_size,int(self.width/2) + (self.width%2-1),wall_height,self.x,self.y,wall_color,1)
        
        # Bottom
        BOTTOM_WALL = create_vertical_wall(-self.width*ts, (self.length-1)*ts, 25, self.tile_size, self.width, wall_height, self.x, self.y, wall_color, 1)
        BOTTOM_LEFT = create_vertical_wall(-self.width*ts, (self.length-1)*ts, 25, self.tile_size, int(self.width/2) + (self.width%2), wall_height, self.x, self.y, wall_color, 1)
        BOTTOM_RIGHT = create_vertical_wall(-self.width*ts + (self.width/2+1)*self.tile_size, (self.length-1)*ts,25,self.tile_size,int(self.width/2) + (self.width%2-1),wall_height,self.x,self.y,wall_color,1)
        
        if "t" in door_at:
            self.walls.extend(TOP_LEFT)
            self.walls.extend(TOP_RIGHT)
        elif "t" not in gap_at:
            self.walls.extend(TOP_WALL)
            
        if "b" in door_at:
            self.walls.extend(BOTTOM_LEFT)
            self.walls.extend(BOTTOM_RIGHT)
        elif "b" not in gap_at:
            self.walls.extend(BOTTOM_WALL)
            
        if "r" in door_at:
            self.walls.extend(RIGHT_TOP)
            self.walls.extend(RIGHT_BOTTOM)
        elif "r" not in gap_at:
            self.walls.extend(RIGHT_WALL)
                    
        if "l" in door_at:
            self.walls.extend(LEFT_TOP)
            self.walls.extend(LEFT_BOTTOM)
        elif "l" not in gap_at:
            self.walls.extend(LEFT_WALL)
            
class TUNNEL(AREA):
    def __init__(self, x, y, width, length, tile_size=50, type="VERTICAL", wall_color=(0.08, 0.10, 0.13, 1), floor_color=(0.12, 0.10, 0.08, 1)):
        super().__init__(x, y, width, length, tile_size, floor_color)
        
        wall_height = 100
        ts = self.tile_size*0.5
        LEFT = create_vertical_wall((self.width-1)*ts, -self.length*ts, 25, self.tile_size, self.length, wall_height, self.x, self.y, wall_color, 0)
        RIGHT = create_vertical_wall(-self.width*ts-20, -self.length*ts, 25, self.tile_size, self.length, wall_height, self.x, self.y, wall_color, 0)
        TOP = create_vertical_wall(-self.width*ts, -self.length*ts-20, 25, self.tile_size, self.width, wall_height, self.x, self.y, wall_color, 1)
        BOTTOM = create_vertical_wall(-self.width*ts, (self.length-1)*ts, 25, self.tile_size, self.width, wall_height, self.x, self.y, wall_color, 1)
        
        if "t" in type:
            self.walls.extend(TOP)
        if "b" in type:
            self.walls.extend(BOTTOM)
        if "l" in type:
            self.walls.extend(LEFT)
        if "r" in type:
            self.walls.extend(RIGHT)



class Player:
    health = 100
    max_health = 100
    
    shield = 100
    max_shield = 100
    
    moving = False
    moved = 0
    speed = 0
    acc = 300
    
    angle = 0
    rotated = 0
    rotating = False
    rotation_direction = 0
    rotation_speed = 10
    rotation_acc = 1
    
    
    keys = []
    
    leg_angle = 0
    leg_angle_dir = 1
    leg_angle_limit = 20
    
    armor_on = False
    
    on_air = False
    speedZ = 0
    jump_acc = 150
    
    attack_on = False
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.width = 30
        self.depth = 10
        self.height = 80
        self.z = self.height//2
        self.keys = []
        
    def jump(self):
            if self.on_air:
                return
            self.on_air = True
            self.speedZ = 10
        
    def jump_update(self):
        self.z += self.speedZ
        self.speedZ -= 0.5
        if self.z <= self.height // 2:
            self.z = self.height // 2
            self.speedZ = 0
            self.on_air = False
        if self.on_air:
            self.move(1)
    
    def draw(self):
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        
        glPushMatrix()
        
        
        # if self.armor_on:
        #     # Halmet
        #     glPushMatrix()
        #     glColor4f(0.10, 0.65, 0.75, 1)
        #     glTranslatef(0, 0, self.height//2 - debug.text_y)
        #     glScalef(self.width*0.4, self.width*0.4, self.width*0.4)
        #     gluSphere(gluNewQuadric(), 1, 20, 20)
        #     glPopMatrix()
        
        # Head
        glPushMatrix()
        glColor4f(0.72, 0.45, 0.25, 1)
        glTranslatef(0, 0, self.height//2 - self.height*0.1)
        glScalef(self.width*0.4, self.width*0.4, self.width*0.4)
        gluSphere(gluNewQuadric(), 1, 20, 20)
        glPopMatrix()
        
        
        # Body
        glPushMatrix()
        glColor4f(0.25, 0.35, 0.12, 1)
        if self.armor_on:
            glColor4f(0.08, 0.55, 0.65, 1)
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
        glColor4f(0.20, 0.12, 0.07, 1)
        if self.armor_on:
            glColor4f(0.06, 0.42, 0.50, 1)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.15)
        glTranslatef(-self.width*0.25, 0, 0)
        glScalef(self.width*0.4, self.depth, self.height*0.3)
        glutSolidCube(1)
        glPopMatrix()
        
        # Right Boot
        glPushMatrix()
        glColor4f(0.12, 0.07, 0.04, 1)
        if self.armor_on:
            glColor4f(0.05, 0.35, 0.42, 1)
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
        glColor4f(0.20, 0.12, 0.07, 1)
        if self.armor_on:
            glColor4f(0.06, 0.42, 0.50, 1)
        glTranslatef(0, 0, -self.height*0.5 + self.height*0.15)
        glTranslatef(self.width*0.25, 0, 0)
        glScalef(self.width*0.4, self.depth, self.height*0.3)
        glutSolidCube(1)
        glScalef(1/(self.width*0.4), 1/self.depth, 1/(self.height*0.3))
        glPopMatrix()
        
        # Left Boot
        glPushMatrix()
        glColor4f(0.12, 0.07, 0.04, 1)
        if self.armor_on:
            glColor4f(0.05, 0.35, 0.42, 1)
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
        glColor4f(0.72, 0.45, 0.25, 1)
        glTranslatef(self.width*0.6, 0, self.height*0.1)
        glScalef(self.width*0.2, self.depth, self.height*0.4)
        glutSolidCube(1)
        glPopMatrix()
        
        # Left Shoulder
        glPushMatrix()
        glColor4f(0.25, 0.35, 0.12, 1)
        if self.armor_on:
            glColor4f(0.07, 0.45, 0.52, 1)
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
        glColor4f(0.72, 0.45, 0.25, 1)
        glTranslatef(-self.width*0.6, 0, self.height*0.1)
        glScalef(self.width*0.2, self.depth, self.height*0.4)
        glutSolidCube(1)
        glPopMatrix()
        
        # Right Shoulder
        glPushMatrix()
        glColor4f(0.25, 0.35, 0.12, 1)
        if self.armor_on:
            glColor4f(0.07, 0.45, 0.52, 1)
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
            new_sheild = self.shield - point*1.5
            if new_sheild > 0:
                self.shield = new_sheild
            else:
                self.shield = 0
            if self.shield <= 0:
                self.armor_on = False
        else:
            new_health = self.health - point
            if new_health > 0:
                self.health = new_health
            else:
                self.health = 0

    def move(self, direction):
        acc = self.acc
        if self.on_air:
            acc = self.jump_acc
        self.speed += acc * dt * direction
    
    def rotate(self, direction):
        player.rotation_direction = direction
        player.rotating = True  

    def attack(self):
        pass
    
    def update(self):
        if self.rotating:
            self.angle += self.rotation_speed * self.rotation_direction
            self.rotated += 1
            if self.rotated >= self.rotation_acc:
                self.rotated = 0
                self.rotating = False
        
        theta = math.radians(self.angle)
        dx = math.sin(theta) * self.speed
        dy = -math.cos(theta) * self.speed
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        move_x = True
        move_y = True
        
        for room in room_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 15))
            move_y = (move_y and not room.collision_detection(self.x, new_y, 15))
        
        for item in item_list:
            move_x = (move_x and not item.collision_detection(new_x, self.y, 15))
            move_y = (move_y and not item.collision_detection(self.x, new_y, 15))
        
        if abs(self.x - new_x) > 0.1 or abs(self.y - new_y) > 0.1:
            self.move_leg()
        else:
            self.leg_angle = 0
            
        if move_x:
            self.x = new_x
            
        if move_y:
            self.y = new_y
            
        self.speed *= 0.5
        
        self.jump_update()

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
        draw_text(-350, 205, f"Player {int(player.health)}/100")
        bar_color = (0, 1, 0)
        if player.health < 20:
            bar_color = (1, 0, 0)
        elif player.health < 50:
            bar_color = (1, 1, 0)
        draw_rect(-275 - (150 - (150 * (player.health/100)))//2, 210, 150 * (player.health/100), 20, bar_color)
        
    def draw_player_shield(self):
        if not player.armor_on:
            return
        draw_text(-350, 180, f"Shield {int(player.shield)}/100")
        bar_color = (0.10, 0.65, 0.75)
        draw_rect(-275 - (150 - (150 * (player.shield/100)))//2, 185, 150 * (player.shield/100), 20, bar_color)
        
    def draw_fps(self):
        fps = math.ceil(1/dt)
        draw_text(280, 240, f"FPS: {fps}")
    
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
            
            
        # Restore original projection and modelview matrices
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def update(self):
        pass


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
        
        glColor4f(0.25, 0.10, 0.03, 1)
        glTranslatef(0, 0, -0.1*self.height)
        glScale(self.width, self.depth, 0.8*self.height)
        glutSolidCube(1)
        glScale(1/self.width, 1/self.depth, 1/(0.8*self.height))
        
        glColor4f(1, 1, 0, 1)
        glTranslatef(0, 0, 0.5*self.height)
        glScale(self.width, self.depth, 0.2*self.height)
        glutSolidCube(1)
        
        glPopMatrix()

class SKULL(STATIC_OBJECT):
    def __init__(self, x, y, z, width, height, depth, angle, isLightSource=False):
        super().__init__(x, y, z, width, height, depth, isLightSource)
        self.angle = angle
        
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(0.5, 0.5, 0.5)
        glScalef(self.width, self.depth, self.height)
        
        # Skull
        glColor3f(0.75, 0.72, 0.62)

        # Head
        glPushMatrix()
        glScalef(1.0, 0.85, 1.0)
        glutSolidSphere(20, 12, 8)
        glPopMatrix()

        # Jaw
        glPushMatrix()
        glTranslatef(0, 2, -15)
        glScalef(0.65, 0.55, 0.45)
        glutSolidCube(20)
        glPopMatrix()

        # Eye sockets
        glColor3f(0.02, 0.02, 0.02)

        glPushMatrix()
        glTranslatef(-8, -17, 5)
        glutSolidSphere(5, 8, 6)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(8, -17, 5)
        glutSolidSphere(5, 8, 6)
        glPopMatrix()

        # Nose
        glPushMatrix()
        glTranslatef(0, -18, -3)
        glScalef(0.5, 0.4, 0.8)
        glutSolidCone(5, 8, 6, 1)
        glPopMatrix()

        # Teeth
        glColor3f(0.85, 0.82, 0.72)

        for x in [-7, -3.5, 0, 3.5, 7]:
            glPushMatrix()
            glTranslatef(x, -18, -14)
            glScalef(0.25, 0.3, 0.5)
            glutSolidCube(8)
            glPopMatrix()

        glPopMatrix()

class HINT_ARROW(STATIC_OBJECT):
    def __init__(self, x, y, z, width, depth, height, isLightSource=False):
        super().__init__(x, y, z, width, height, depth, isLightSource)
        self.d = 0
        self.angle = 0
        self.upward = True
        
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        glTranslatef(0, 0, self.d)
        
        
        glColor4f(1.0, 0.84, 0.2, 0.8)
        glPushMatrix()
        glScalef(self.width, self.depth, self.height)
        glutSolidCube(1)
        glPopMatrix()
        
        glColor4f(1.0, 0.45, 0.0, 0.8)
        glPushMatrix()
        glTranslatef(0, 0, -self.height*0.5)
        glRotatef(45, 1, 0, 0)
        glScalef(self.width+1, self.width+1, self.width+1)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        
    def update(self):
        if self.upward:
            self.d += 0.2
        else:
            self.d -= 0.2
            
        if self.d > 10 or self.d <= -10:
            self.upward = not self.upward
        self.angle += 1

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
        door_color = (0.22, 0.09, 0.025)
        glColor4f(0.18, 0.17, 0.15, 1)
        glScalef(self.width, 5, self.height)
        glutSolidCube(1)
        glScalef(1/self.width, 1/5, 1/self.height)
        glTranslatef(self.width/2 - 6, 0, 0)
        glColor4f(1, 1, 0, 1)
        glutSolidCube(6)
        glPopMatrix()
        
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.width:
            if self.locked:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "[LOCKED]")
            elif self.closed:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "Press \'f\'")
    
    def update(self):
        if self.closed:
            if self.angle > 0:
                self.angle -= 100 * dt
        else:
            if self.angle < 90:
                self.angle += 100 * dt
        
    def keyboard_listener(self, key):
        if key == b'f' and self.closed:
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


# INTERACTIVE ITEMS
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
        if not self.visible:
            return
        r, g, b = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, 30)
        glRotatef(self.rotation, 0, 0, 1)
        
        glColor4f(r, g, b, 1)
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


class KEY(ITEM):
    def __init__(self, x, y, z, width, height, depth, radius, color, visible=True, active=True, callback=None, rotation=0, name="KEY_X"):
        super().__init__(x, y, z, width, height, depth, radius, color, visible, active, callback, rotation, isLightSource=True)
        self.name = name
    
    def draw(self):
        if not self.visible:
            return
        r, g, b = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, 30)
        glRotatef(self.rotation, 0, 0, 1)
        
        glColor4f(r, g, b, 1)
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
        
    def callBack(self):
        self.visible = False
        self.active = False
        player.keys.append((self.name, self.color))

class HEALTH(ITEM):
    def __init__(self, x, y, z, width, height, depth, radius, color=(0, 1, 0, 1), visible=True, active=True, callback=None, rotation=0, isLightSource=False):
        super().__init__(x, y, z, width, height, depth, radius, color, visible, active, callback, rotation, isLightSource)
        
    def draw(self):
        if not self.visible:
            return
        r, g, b = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, 30)
        glRotatef(self.rotation, 0, 0, 1)
        
        glColor4f(0, 1, 0, 1)
        
        glPushMatrix()
        glScalef(self.width, self.depth, self.height*0.5)
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glScalef(self.width, self.depth, self.height*0.5)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        
    def callBack(self):
        self.visible = False
        self.active = False
        if player.health + 5 <= player.max_health:
            player.health += 5

# TRAPS
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
        glColor4f(0.18, 0.16, 0.14, 1)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.width, self.width, 1)
        glutSolidCube(1)
        glScalef(1/self.width, 1/self.width, 1)
        
        glColor4f(0.32, 0.35, 0.38, 1)
        glTranslatef(self.width/2 - 6, -self.width//2 + 8, 0)
        for j in range(4):
            for i in range(4):
                gluCylinder(gluNewQuadric(), self.width/10, 0, 30, 10, 10)
                glTranslatef(-self.width/4, 0, 0)
            glTranslatef(self.width, self.width/4, 0)
            
        glTranslatef(0, -self.width, 18)
        
        glColor4f(0.55, 0.58, 0.62, 1)
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
            theta = math.radians(player.angle)
            fx = math.sin(theta)
            fy = -math.cos(theta)
            dx = player.x - self.x
            dy = player.y - self.y
            distance = math.hypot(dx, dy)
            dx = dx/distance
            dy = dy/distance
            
            dot = -(dx * fx + dy * fy)
            if dot < 0:
                player.speed += 20
            else:
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
        glColor4f(0.45, 0.10, 0.55, 1)
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.width, self.width, 1)
        glutSolidCube(1)
        glScalef(1/self.width, 1/self.width, 1)
        
        glColor4f(0.40, 0.75, 0.05, 1)
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

class ENEMY:
    def __init__(self, x, y, z, width, depth, height, radius=30):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.height = height
        self.radius = radius
        
        self.speed = 0
        self.accelaration = 30
        
        self.attack_cooldown = 0
        
        self.detected_player = False
        
        self.init_point = (self.x, self.y)
        
        self.angle = 0
        
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)
        # glRotatef(90, 0, 0, 1)
        glRotatef(self.angle, 0, 0, 1)
        glColor3f(1, 1, 1)
        
        glPushMatrix()
        glScalef(self.width, self.depth, self.height)
        glutSolidCube(1)
        glPopMatrix()
        
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(0, 5, 0)
        glutSolidCube(5)
        glPopMatrix()
        
        glPopMatrix()
    
    def attack(self):
        if self.attack_cooldown < 0.5:
            player.damage(20)
            player.speed -= 10
            self.attack_cooldown = 100
        self.attack_cooldown -= 1
        
    def collision_detection(self):
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        if distance < self.radius + 30:
            self.attack()
            pass
        
    def face_toward_player(self):
        px = self.init_point[0]
        py = self.init_point[1]
        if self.detected_player:
            px = player.x
            py = player.y
        
        dx = px - self.x
        dy = py - self.y

        dx *= -1

        target_angle = math.degrees(math.atan2(dx, dy))

        difference = (target_angle - self.angle + 180) % 360 - 180

        if difference > 1:
            self.angle = (self.angle + 1) % 360
        elif difference < -1:
            self.angle = (self.angle - 1) % 360
        else:
            self.angle = target_angle
            return True

        return False
            
    def update(self):
        move_x = True
        move_y = True
        
        distance = math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)
        
        if distance < 400:
            self.detected_player = True
        else:
            self.detected_player = False
        
        if self.detected_player:
            dx = player.x - self.x
            dy = player.y - self.y
            self.collision_detection()
        else:
            dx = self.init_point[0] - self.x
            dy = self.init_point[1] - self.y
            
        if dx != 0:
            dx = dx/abs(dx)
        if dy != 0:
            dy = dy/abs(dy)
        
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        
        
        distance = math.sqrt((new_x - player.x)**2 + (new_y - player.y)**2)
        do_move_forward = self.face_toward_player()
        
        for room in room_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 10))
            move_y = (move_y and not room.collision_detection(self.x, new_y, 10))
        
        
        if distance > 30 and distance > 90 and do_move_forward:
            if move_x:
                self.x = new_x
            if move_y:
                self.y = new_y
            pass
        
        self.speed *= 0.5
        self.speed += self.accelaration


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

def draw_point(size, x, y, z, color=(1,1,1,1)):
    r, g, b, a = color
    glColor4f(r, g, b, 1)
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
    
    glColor4f(r, g, b, 1)
    glVertex3f(x+width//2, y-height//2, 0)
    
    glColor4f(r1, g1, b1, 1)
    glVertex3f(x-width//2, y-height//2, 0)
    
    glColor4f(r2, g2, b2, 1)
    glVertex3f(x-width//2, y+height//2, 0)
    
    glColor4f(r3, g3, b3, 1)
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
    
    global FIRST_PERSON, KEY_W, KEY_S, text_x, text_y, GAME_STATE, CHEAT_MODE
    if GAME_STATE == "GAME":
        if key == b'w':
            player.move(1)
        if key == b's':
            player.move(-1)
        if key == b'a':
            player.rotate(1)
        if key == b'd':
            player.rotate(-1)
        
        if key == b'u':
            room_to_move.y -= 10
            debug.text_y += 1
            pass
        if key == b'j':
            room_to_move.y += 10
            debug.text_y -= 1
            pass
        if key == b'h':
            room_to_move.x += 10
            debug.text_x -= 1
            pass
        if key == b'k':
            room_to_move.x -= 10
            debug.text_x += 1
            pass
            
        if key == b'z':
            player.armor_on = not player.armor_on
            
        if key == b'v':
            FIRST_PERSON = not FIRST_PERSON
            
        if key == b'c':
            CHEAT_MODE = not CHEAT_MODE
            
        if key == b' ':
            print(room_to_move.x, room_to_move.y)
            # print(debug.text_x, debug.text_y)
            player.jump()
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
    # print(key)
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

import time
last_time = time.time()
FPS = 60
target_time = 1/FPS
dt = 1

def idle(value=0):
    global last_time, dt
    
    current_time = time.time()
    dt = current_time - last_time
    if dt < 1/FPS:
        return
    dt = target_time
    last_time = current_time
    
    if GAME_STATE == 'GAME':
        player.update()
        camera.update()
        hud.update()
        
        for item in item_list:
            item.update()
            
        for item in static_item_list:
            item.update()
            
        for trap in trap_list:
            trap.update()
            
        for enemy in enemy_list:
            enemy.update()
        
    glutPostRedisplay()

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
hint_arrow_list = []

room_to_move = None
player = None
hud = None

def game_init():
    global item_list, static_item_list, room_list, room_to_move, player, hud, enemy_list, trap_list, hint_arrow_list
    
    player = Player(0, 0)
    hud = HUD()
    
    room_list = [
        ROOM(0, 0, 10, 10, 50, door_at='t'),
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
    ]
    
    item_list = [
        KEY(-1440, -350, 0, 20, 20, 20, 20, (1, 0, 0), name="0x0001"),
        ESCAPE_DOOR(610, -1270, 50, 50, 100, required_key_name="0x0001"),
        HEALTH(0, -100, 0, 10, 10, 20, 20, (1, 0, 1))
    ]
    
    trap_list = [
        SPIKETRAP(-740, -710, 0, 50, 30),
        SPIKETRAP(-790, -710, 0, 50, 30),
        SPIKETRAP(-840, -710, 0, 50, 30),
        SPIKETRAP(-890, -710, 0, 50, 30),
        POISONTRAP(-1440, -350, 0, 50, 2),
    ]
    
    static_item_list = [
        SKULL(-900, -960, 10, 1, 1, 1, 90 + 45, False),
        TORCH(-1690, -140, 25, 10, 50, 10),
        TORCH(-1690, -610, 25, 10, 50, 10),
        TORCH(40, -250, 25, 10, 50, 10),
        TORCH(-50, -250, 25, 10, 50, 10),
    ]
    
    hint_arrow_list = [
        HINT_ARROW(-10, -270, 150, 10, 10, 30),
        HINT_ARROW(-10, -890, 150, 10, 10, 30),
        HINT_ARROW(-800, -890, 150, 10, 10, 30),
        HINT_ARROW(-800, -400, 150, 10, 10, 30),
        HINT_ARROW(-1210, -340, 150, 10, 10, 30),
    ]
    
    # static_item_list.extend(hint_arrow_list)
    
    enemy_list = [
        # ENEMY(-210, -230, 25, 30, 10, 80),
        # ENEMY(-210, 170, 25, 30, 10, 80),
    ]

    room_to_move = HINT_ARROW(-800, -400, 150, 10, 10, 30)
    # static_item_list.append(room_to_move)

game_init()
 
def draw_menu():
    glColor4f(1, 0, 0, 1)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(-12*5, 200, "3D Dungeon Escape", font=GLUT_BITMAP_TIMES_ROMAN_24)
    
    start_button.draw()
    help_button.draw()
    exit_button.draw()

def draw_help():
    glColor4f(1, 0, 0, 1)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(0, WINDOW_SIZE[1]//2 - 100, "HELP", font=GLUT_BITMAP_TIMES_ROMAN_24)
    help_back_button.draw()

def draw_game():
    for room in room_list:
        room.draw()
        
    for item in item_list:
        distance = math.sqrt((player.x - item.x)**2 + (player.y - item.y)**2)
        if distance < 1000:
            item.draw()
        
    for item in static_item_list:
        distance = math.sqrt((player.x - item.x)**2 + (player.y - item.y)**2)
        if distance < 1000:
            item.draw()
            
    for item in hint_arrow_list:
        distance = math.sqrt((player.x - item.x)**2 + (player.y - item.y)**2)
        if distance < 1000 and CHEAT_MODE:
            item.draw()
        
    for trap in trap_list:
        distance = math.sqrt((player.x - trap.x)**2 + (player.y - trap.y)**2)
        if distance < 1000:
            trap.draw()
        
    for enemy in enemy_list:
        enemy.draw()
        
    player.draw()
    hud.draw()

def draw_escaped():
    glColor4f(1, 0, 0, 1)
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

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
