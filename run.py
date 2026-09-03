# Member 1: Jubayer Iqbal [24101512]
# Member 2: Yeasin Arafat Rabby [24101120]
# Member 3: Md Atikullah Tanvir [24101186]
# Group: 05
# Section: 08

# Premitives -
    # glutSolidCube(30)
    # gluSphere(gluNewQuadric(), 20, 10, 10)
    # gluCylinder(gluNewQuadric(), 8, 3, 30, 10, 10)
    # draw_text(10, 730, f"Player Bullet Missed: {player.missed}")

import os
os.environ["PYOPENGL_PLATFORM"] = "glx"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random

WINDOW_SIZE = (720, 520)
WINDOW_TITLE = b"3D Dungeon Escape"
fovY = 120  # Field of view

# GAME CONSTANTS
CHEAT_MODE = False
VIEW_MODE = 1
PAUSE = False
SECONDS = 0

last_time = time.time()
dt = 1

# GAME_STATE
#   - MENU
#   - HELP
#   - ROOM SELECT
#   - GAME
#   - ESCAPED
GAME_STATE = "MENU"
ROOM_LEVEL = 1
DRAWING_RADIUS = 1000


def updateLevel():
    global ROOM_LEVEL
    ROOM_LEVEL += 1

def getDistance(obj1_x, obj1_y, obj2_x, obj2_y):
    distance = math.sqrt((obj1_x - obj2_x)**2 + (obj1_y - obj2_y)**2)
    return distance

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
        
    def click(self, mouseX, mouseY, callback=None, *args):
        if self.x - self.width//2 < mouseX < self.x + self.width//2 and self.y - self.height//2 < mouseY < self.y + self.height//2:
            if callback is not None:
                callback(*args)

class CAMERA:
    camera_x = 0
    camera_y = 0
    camera_z = 0

    target_x = 0
    target_y = 0
    target_z = 0
    
    target_up = 45

    def __init__(self):
        self.distance = 40
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.target_x, self.target_y, self.target_z)
        glColor3f(1, 1, 1)
        glutSolidCube(1)
        glPopMatrix()

    def update(self):
        theta = math.radians(player.angle)
        fx = math.sin(theta)
        fy = -math.cos(theta)
        
        if self.target_up >= 45:
            self.target_up = 45
        elif self.target_up <= -25:
            self.target_up = -25
        
        if VIEW_MODE == 0:
            self.camera_x = player.x + fx * 20
            self.camera_y = player.y - fy * -20
            self.camera_z = player.z + player.height//2
            
            self.target_x = player.x + fx * self.distance * 2
            self.target_y = player.y + fy * self.distance * 2
            self.target_z = player.z + player.height//2
            
        elif VIEW_MODE == 1:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            self.camera_z = player.z + player.height + self.target_up
            
            self.target_x = player.x + fx * self.distance
            self.target_y = player.y + fy * self.distance
            self.target_z = player.z + player.height//2
            
        elif VIEW_MODE == 2:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            
            self.camera_x = player.x
            self.camera_y = player.y + self.distance
            self.camera_z = 500
            
            self.target_x = player.x
            self.target_y = player.y
            self.target_z = 0
        else:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            
            self.camera_x = player.x
            self.camera_y = player.y + self.distance
            self.camera_z = 1000
            
            self.target_x = player.x
            self.target_y = player.y
            self.target_z = 0



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
        
        self.max_lightness = 1.5
        self.lightness = 0
        self.l_dir = 1
        
    def draw(self):
        r, g, b, a = self.color
        distance = getDistance(self.x + self.col_x, self.y + self.col_y, player.x, player.y)
        if distance < 75:
            r += 0.15*self.lightness/self.max_lightness
            g += 0.10*self.lightness/self.max_lightness
            b += 0.04*self.lightness/self.max_lightness

        elif distance < 150:
            r += 0.08*self.lightness/self.max_lightness
            g += 0.05*self.lightness/self.max_lightness
            b += 0.02*self.lightness/self.max_lightness

        elif distance < 250:
            r += 0.03*self.lightness/self.max_lightness
            g += 0.02*self.lightness/self.max_lightness
            b += 0.01*self.lightness/self.max_lightness
        glColor4f(r, g, b, 1)
        
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
        self.lightness += dt * self.l_dir
        if self.lightness >= self.max_lightness or self.lightness <= 0:
            self.l_dir *= -1
    
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
        
        self.max_lightness = 3
        self.lightness = 0
        self.l_dir = 1
            
    def floor_light_up(self, rect_x, rect_y, obj_x, obj_y, color, lightness, max_lightness):
        r, g, b, a = color
        distance = math.sqrt((rect_x + self.x - obj_x)**2 + (rect_y + self.y - obj_y)**2)
        if distance < 75:
            r += 0.15*lightness/max_lightness
            g += 0.10*lightness/max_lightness
            b += 0.04*lightness/max_lightness

        elif distance < 150:
            r += 0.08*lightness/max_lightness
            g += 0.05*lightness/max_lightness
            b += 0.02*lightness/max_lightness

        elif distance < 250:
            r += 0.03*lightness/max_lightness
            g += 0.02*lightness/max_lightness
            b += 0.01*lightness/max_lightness
        return r, g, b, a
        
    def draw_floor(self):
        for j in range(-self.length//2, self.length//2, 1):
            for i in range(-self.width//2, self.width//2, 1):
                color = self.floor_color
                if (i + j) % 2 == 0:
                    color = (0.08, 0.08, 0.08, 1)
                else:
                    color = (0.02, 0.02, 0.02, 1)
                    
                rect_x = i*(self.tile_size + 0)
                rect_y = j*(self.tile_size + 0)
                r, g, b, a = color
                
                distance = getDistance(rect_x + self.x, rect_y + self.y, player.x, player.y)
                if distance > DRAWING_RADIUS:
                    continue
                
                r, g, b, a = self.floor_light_up(rect_x, rect_y, player.x, player.y, (r, g, b, a), self.lightness, self.max_lightness)
                    
                for item in static_item_list:
                    if not item.isLightSource:
                        continue
                    r, g, b, a = self.floor_light_up(rect_x, rect_y, item.x, item.y, (r, g, b, a), item.lightness, item.max_lightness)
                        
                for item in item_list:
                    try:
                        if not item.isLightSource:
                            continue
                        if not item.active:
                            continue
                    except Exception as e:
                        print(e)
                        continue
                    r, g, b, a = self.floor_light_up(rect_x, rect_y, item.x, item.y, (r, g, b, a), 0, 3)
                draw_rect(rect_x, rect_y, self.tile_size, self.tile_size, color=(r, g, b))
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        self.draw_floor()
        for obj in self.walls:
            distance = getDistance(obj.x + self.x, obj.y + self.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                obj.draw()
        glPopMatrix()
        
    def collision_detection(self, x, y, radius):
        for obj in self.walls:
            if obj.collision_detection(x, y, radius):
                return True
        return False

    def update(self):
        for wall in self.walls:
            wall.update()
            
        self.lightness += dt * self.l_dir
        if self.lightness >= self.max_lightness or self.lightness <= 0:
            self.l_dir *= -1

class ROOM(AREA):
    def __init__(self, x, y, width, length, tile_size=50, wall_color=(0.1, 0.1, 0.2, 1), floor_color=(0, 0, 0, 1), door_at="tblf", gap_at=""):
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
    def __init__(self, x, y, width, length, tile_size=50, type="VERTICAL", wall_color=(0.1, 0.1, 0.2, 1), floor_color=(0, 0, 0, 1)):
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


class BULLET:
    def __init__(self, x, y, z, dir_x, dir_y, owner):
        self.x = x
        self.y = y
        self.z = z
        self.speed = 500
        
        self.direction_x = dir_x
        self.direction_y = dir_y
        
        self.active = True
        self.owner = owner
        
    def draw(self):
        if not self.active:
            return
        glPushMatrix()
        glTranslatef(self.x ,self.y, self.z)
        glColor3f(0.8, 0.8, 1)
        gluSphere(gluNewQuadric(), 3, 10, 10)
        glPopMatrix()
        
    def update(self):
        if not self.active:
            return
        self.x += self.direction_x * dt * self.speed
        self.y += self.direction_y * dt * self.speed
        
        for enemy in enemy_list:
            if enemy == self.owner:
                continue
            distance = getDistance(self.x, self.y, enemy.x, enemy.y)
            if distance <= enemy.radius:
                self.active = False
                enemy.get_damage(30)
        
        if self.owner != player:
            distance = getDistance(self.x, self.y, player.x, player.y)
            if distance <= player.radius:
                self.active = False
                player.get_damage(self.owner.damage)
                
        
        for room in room_list:
            collided = room.collision_detection(self.x, self.y, 5)
            if collided:
                self.active = False

# Player
class PLAYER:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 100
        
        self.width = 30
        self.depth = 10
        self.height = 60
        self.radius = 30
        
        self.check_point = (x, y)
        
        
        self.life = 3
            
        self.health = 100
        self.max_health = 100
        
        self.shield_on = False
        self.shield = 0
        self.max_shield = 100
        
        self.moving = False
        self.moved = 0
        self.speed = 0
        self.acc = 12000
        self.sprint = False
        self.sprint_acc = 24000
        
        self.angle = 0
        self.rotated = 0
        self.rotating = False
        self.rotation_direction = 0
        self.rotation_speed = 10
        self.rotation_acc = 1
        
        
        self.on_air = False
        self.speedZ = 0
        
        self.damage_cooldown = 0
        
        self.arm_angle = 0
        self.body_angle_direction = 1
        self.body_angle_limit = 30
        self.body_movement_speed = 600
    
        self.attack_on = False
        self.attack_angle = 0
        self.attack_phase = "raise"
        self.attack_speed = 2000
        self.attack_left_arm = False
        
        self.bullets = []
        self.keys = []
         
    def jump(self):
        if not self.on_air:
            self.on_air = True
            self.speedZ = 250
        
    def update_jump(self):
        self.z += self.speedZ * dt
        self.speedZ -= 700 * dt
        
        if self.z <= self.height / 2:
            self.z = self.height / 2
            self.speedZ = 0
            self.on_air = False

        if self.on_air and self.speed != 0:
            direction = self.speed / abs(self.speed)
            self.move(0.45 * direction * dt * 60)
    
    def fire(self):
        if not self.attack_on:
            dx, dy = self.get_face_point()
            self.bullets.append(BULLET(self.x, self.y, self.z + self.height//2, dx, dy, self))
            self.attack()
    
    def attack(self):
        if not self.attack_on:
            self.attack_on = True
            self.attack_phase = "raise"
            self.attack_angle = 0
            self.attack_left_arm = not self.attack_left_arm
        
    def update_attack(self):
        if not self.attack_on:
            return

        if self.attack_phase == "raise":
            self.attack_angle = 140
            self.attack_phase = "swing"

        elif self.attack_phase == "swing":

            self.attack_angle -= 600 * dt

            if self.attack_angle <= 0:
                self.attack_angle = 0
                self.attack_phase = "finished"

        elif self.attack_phase == "finished":

            self.attack_on = False
    
    def draw_player(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)
        
        glutSolidCube(3)
        
        glPopMatrix()
    
    def draw(self):
        self.draw_player()
        for bullet in self.bullets:
            bullet.draw()
    
    def get_damage(self, point):
        if self.damage_cooldown > 0:
            return
        if CHEAT_MODE:
            return
        if self.shield_on:
            new_sheild = self.shield - point*1.5
            if new_sheild > 0:
                self.shield = new_sheild
            else:
                self.shield = 0
            if self.shield <= 0:
                self.shield_on = False
        else:
            new_health = self.health - point
            if new_health > 0:
                self.health = new_health
            else:
                self.health = 0
        self.damage_cooldown = 100

    def move(self, direction):
        acc = self.acc
        if self.sprint:
            acc = self.sprint_acc
        self.speed += acc * dt * direction
    
    def rotate(self, direction):
        player.rotation_direction = direction
        player.rotating = True  

    def move_body(self):
        self.arm_angle += abs(self.speed) * dt * self.body_angle_direction
        
        if self.arm_angle >= self.body_angle_limit:
            self.arm_angle = self.body_angle_limit
            self.body_angle_direction = -1

        elif self.arm_angle <= -self.body_angle_limit:
            self.arm_angle = -self.body_angle_limit
            self.body_angle_direction = 1
    
    def get_face_point(self):
        theta = math.radians(self.angle)
        dx = math.sin(theta)
        dy = -math.cos(theta)
        return dx, dy
    
    def update_move(self):
        
        dx, dy = self.get_face_point()
        dx = dx * self.speed * dt
        dy = dy * self.speed * dt
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        move_x = True
        move_y = True
        
        for room in room_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 15))
            move_y = (move_y and not room.collision_detection(self.x, new_y, 15))
        
        for item in item_list:
            move_x = (move_x and not item.collision_detection(new_x, self.y, 15, self))
            move_y = (move_y and not item.collision_detection(self.x, new_y, 15, self))
        
        if abs(self.x - new_x) > 0.1 or abs(self.y - new_y) > 0.1:
            self.move_body()
        else:
            self.arm_angle = 0
            
        if move_x:
            self.x = new_x
            
        if move_y:
            self.y = new_y
            
        self.speed *= 0.5
        if abs(self.speed) <= 0.5:
            self.speed = 0
    
    def update_rotate(self):
        if self.rotating:
            self.angle += self.rotation_speed * self.rotation_direction
        self.rotated += 1
        if self.rotated >= self.rotation_acc:
            self.rotated = 0
            self.rotating = False
    
    def update_bullet(self):
        for bullet in self.bullets:
            if bullet.active:
                bullet.update()
            else:
                self.bullets.remove(bullet)
    
    def update_life(self):
        if self.life <= 0:
            GAME_STATE = "GAMEOVER"
            
        if self.health <= 0:
            self.life -= 1
            self.health = 100
            self.x, self.y = self.check_point
            self.z += 30
            self.angle = 0
        
        if self.damage_cooldown >= 0:
            self.damage_cooldown -= 1
    
    def update(self):
        global GAME_STATE
        
        self.update_life()
        self.update_rotate()
        self.update_move()
        self.update_jump()
        self.update_attack()
        self.update_bullet()

class ADVENTURER(PLAYER):
    quadric = gluNewQuadric()

    def __init__(self, x, y):
        super().__init__(x, y)

    def cube(self, color, x, y, z, sx, sy, sz):

        glPushMatrix()

        glColor4f(*color)

        glTranslatef(x, y, z)
        glScalef(sx, sy, sz)

        glutSolidCube(1)

        glPopMatrix()

    def sphere(self, color, x, y, z, sx, sy, sz):

        glPushMatrix()

        glColor4f(*color)

        glTranslatef(x, y, z)
        glScalef(sx, sy, sz)

        gluSphere(
            ADVENTURER.quadric,
            1,
            10,
            8)

        glPopMatrix()

    def draw_leg(self, side):

        W = self.width
        D = self.depth
        H = self.height

        glPushMatrix()

        glTranslatef(side * W * 0.22, 0, -H * 0.28)

        # Opposite leg movement
        glRotatef(self.arm_angle * side, 1, 0, 0)

        # Leg
        self.cube(
            (0.12, 0.13, 0.15, 1),
            0,
            0,
            -H * 0.12,

            W * 0.32,
            D * 0.75,
            H * 0.35
        )

        # Boot
        self.cube(
            (0.06, 0.05, 0.04, 1),

            0,
            -D * 0.18,
            -H * 0.32,

            W * 0.38,
            D * 1.15,
            H * 0.16
        )

        glPopMatrix()

    def draw_arm(self, side):

        W = self.width
        D = self.depth
        H = self.height

        glPushMatrix()

        glTranslatef(
            side * W * 0.55,
            0,
            H * 0.22
        )

        # Walking animation
        if self.attack_on:
            if side == -1:
                glRotatef(
                    -self.attack_angle,
                    1, 0, 0
                )

        else:

            glRotatef(
                -self.arm_angle * side,
                1, 0, 0
            )

        # Upper + lower arm
        self.cube(
            (0.18, 0.20, 0.23, 1),

            0,
            0,
            -H * 0.15,

            W * 0.22,
            D * 0.70,
            H * 0.40
        )

        # Hand
        self.sphere(
            (0.55, 0.32, 0.20, 1),

            0,
            0,
            -H * 0.38,

            W * 0.20,
            D * 0.70,
            W * 0.20
        )

        glPopMatrix()

    def draw_body(self):

        W = self.width
        D = self.depth
        H = self.height

        # Tunic / torso
        if self.shield_on:
            torso_color = (0.0, 0.8, 1.0, 1)
        else:
            torso_color = (0.16, 0.20, 0.25, 1)
        self.cube(
            torso_color,

            0,
            0,
            H * 0.04,

            W * 0.85,
            D,
            H * 0.48
        )

        # Belt
        self.cube(
            (0.25, 0.12, 0.05, 1),

            0,
            0,
            -H * 0.18,

            W * 0.90,
            D * 1.05,
            H * 0.08
        )

        # Belt buckle
        self.cube(
            (0.85, 0.60, 0.10, 1),

            0,
            -D * 0.55,
            -H * 0.18,

            W * 0.13,
            D * 0.04,
            H * 0.12
        )

    def draw_head(self):

        W = self.width
        D = self.depth
        H = self.height

        # Neck
        self.cube(
            (0.55, 0.32, 0.20, 1),

            0,
            0,
            H * 0.40,

            W * 0.25,
            D * 0.25,
            W * 0.22
        )

        # Head
        self.sphere(
            (0.55, 0.32, 0.20, 1),

            0,
            0,
            H * 0.55,

            W * 0.40,
            W * 0.40,
            W * 0.40
        )

        # Hair
        self.sphere(
            (0.08, 0.05, 0.03, 1),

            0,
            0,
            H * 0.67,

            W * 0.43,
            W * 0.43,
            W * 0.25
        )

        # Eyes
        for x in (-W * 0.12, W * 0.12):

            self.cube(
                (0.05, 0.05, 0.05, 1),

                x,
                -W * 0.38,
                H * 0.57,

                W * 0.055,
                W * 0.025,
                W * 0.055
            )

    def draw_cape(self):

        W = self.width
        D = self.depth
        H = self.height
        
        if self.shield_on:
            cape_color = (0.0, 0.5, 1.0, 1)
            
        else:
            cape_color = (0.20, 0.04, 0.04, 1)

        self.cube(
            cape_color,

            0,
            D * 0.5,
            0,

            W * 0.70,
            D * 0.10,
            H * 0.65
        )

    def draw_player(self):

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)

        # Body
        self.draw_body()

        # Legs
        self.draw_leg(-1)
        self.draw_leg(1)

        # Arms
        self.draw_arm(-1)
        self.draw_arm(1)

        # Head
        self.draw_head()

        # Cape
        self.draw_cape()

        glPopMatrix()    


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
        draw_text(-350, 180, f"Shield {int(player.shield)}/100")
        bar_color = (0.10, 0.65, 0.75)
        draw_rect(-275 - (150 - (150 * (player.shield/100)))//2, 185, 150 * (player.shield/100), 20, bar_color)
        
    def draw_fps(self):
        fps = math.ceil(1/dt)
        draw_text(280, 240, f"FPS: {fps}")
        
    def draw_time(self):
        global SECONDS
        s = int(SECONDS)
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
        draw_text(-WINDOW_SIZE[0]//2 + 10, WINDOW_SIZE[1]//2 - 150, f"Life: {player.life}")
        
    def draw_level_text(self):
        draw_text(265, 200, f"Level: {ROOM_LEVEL}")
    
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
        
        if PAUSE:
            draw_text(-50, 0, "PAUSED")
        
        if CHEAT_MODE:
            draw_text(-100, 200, "[CHEAT MODE: ON]")
            
            
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
        self.l_dir = 1
        self.lightness = 0
        self.max_lightness = 1
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor4f(1, 1, 1, 1)
        
        glutSolidCube(10)
        
        glPopMatrix()
        
    def update(self):
        pass
    
class TORCH(STATIC_OBJECT):
    quadric = gluNewQuadric()
    
    def __init__(self, x, y, z, width, height, depth):
        super().__init__(x, y, z, width, height, depth, isLightSource=True)
        
    def update(self):
        super().update()
        self.lightness += dt*self.l_dir
        if self.lightness >= self.max_lightness or self.lightness <= 0:
            self.l_dir *= -1

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        # WOODEN HANDLE
        glColor4f(0.25, 0.10, 0.03, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.30)
        glScalef(self.width / 30 * 0.45, self.depth / 30 * 0.45, self.height / 30 * 0.60)
        glutSolidCube(30)
        glPopMatrix()

        # METAL HOLDER
        glColor4f(0.15, 0.15, 0.15, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.58)
        glScalef(self.width / 30 * 0.80, self.depth / 30 * 0.80, self.height / 30 * 0.12)
        glutSolidCube(30)
        glPopMatrix()

        # OUTER FLAME
        glColor4f(1.0, 0.18, 0.01, 1)
        g = 0.5 + (0.50 - 0.18)*self.lightness/self.max_lightness
        b = 0.02 + (0.02 - 0.01)*self.lightness/self.max_lightness
        # print(g, b)
        glColor4f(1.0, g, b, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.75)
        glScalef(self.width / 20 * 0.75, self.depth / 20 * 0.75, self.height / 20 * 0.25)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # MIDDLE FLAME
        glColor4f(1.0, 0.50, 0.02, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.82)
        glScalef(self.width / 20 * 0.50, self.depth / 20 * 0.50, self.height / 20 * 0.20)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # INNER FLAME
        glColor4f(1.0, 0.90, 0.10, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.80)
        glScalef(self.width / 20 * 0.30, self.depth / 20 * 0.30, self.height / 20 * 0.14)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # FLAME TIP
        glColor4f(1.0, 0.30, 0.01, 1)
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.96)
        glScalef(self.width / 30 * 0.35, self.depth / 30 * 0.35, self.height / 30 * 0.25)
        gluCylinder(self.quadric, 8, 3, 30, 10, 10)
        glPopMatrix()
        glPopMatrix()

class SKULL(STATIC_OBJECT):
    quadric = gluNewQuadric()
    
    def __init__(self, x, y, z, width, height, depth, angle, isLightSource=False):
        super().__init__(x, y, z, width, height, depth, isLightSource)
        self.angle = angle

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)

        glColor3f(0.78, 0.75, 0.64)

        # MAIN CRANIUM
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.12)
        glScalef(self.width / 40, self.depth / 40, self.height / 42)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # LOWER SKULL
        glPushMatrix()
        glTranslatef(0, -self.depth * 0.18, -self.height * 0.12)
        glScalef(self.width / 50, self.depth / 45, self.height / 65)
        glutSolidCube(30)
        glPopMatrix()

        # LEFT CHEEK
        glPushMatrix()
        glTranslatef(-self.width * 0.32, -self.depth * 0.25, -self.height * 0.08)
        glScalef(self.width / 100, self.depth / 75, self.height / 100)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # RIGHT CHEEK
        glPushMatrix()
        glTranslatef(self.width * 0.32, -self.depth * 0.25, -self.height * 0.08)
        glScalef(self.width / 100, self.depth / 75, self.height / 100)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # LEFT EYE SOCKET
        glColor3f(0.02, 0.02, 0.02)
        glPushMatrix()
        glTranslatef(-self.width * 0.23, -self.depth * 0.43, self.height * 0.12)
        glScalef(self.width / 90, self.depth / 80, self.height / 90)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # RIGHT EYE SOCKET
        glPushMatrix()
        glTranslatef(self.width * 0.23, -self.depth * 0.43, self.height * 0.12)
        glScalef(self.width / 90, self.depth / 80, self.height / 90)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        # NOSE HOLE
        glColor3f(0.02, 0.02, 0.02)
        glPushMatrix()
        glTranslatef(0, -self.depth * 0.47, -self.height * 0.08)
        glScalef(self.width / 120, self.depth / 100, self.height / 100)
        gluSphere(self.quadric, 20, 10, 10)
        glPopMatrix()

        glPopMatrix()

class BONE(STATIC_OBJECT):
    def __init__(self, x, y, z, width, height, depth, angle, isLightSource=False):
        super().__init__(x, y, z, width, height, depth, isLightSource)
        self.angle = angle

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 0, 1)

        glColor3f(0.78, 0.75, 0.64)

        # SHAFT
        glPushMatrix()
        glTranslatef(-self.width * 0.35, 0, 0)
        glRotatef(90, 0, 1, 0)
        glScalef(self.depth / 30, self.depth / 30, self.width / 30)
        gluCylinder(gluNewQuadric(), 8, 3, 30, 10, 10)
        glPopMatrix()
        
        # LEFT END
        glPushMatrix()
        glTranslatef(-self.width * 0.50, 0, 0)
        glScalef(self.depth / 40, self.depth / 40, self.depth / 40)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glPopMatrix()

        # RIGHT END
        glPushMatrix()
        glTranslatef(self.width * 0.50, 0, 0)
        glScalef(self.depth / 38, self.depth / 38, self.depth / 38)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glPopMatrix()

        # LEFT SMALL BUMP
        glPushMatrix()
        glTranslatef(-self.width * 0.38, 0, self.depth * 0.12)
        glScalef(self.depth / 55, self.depth / 55, self.depth / 55)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glPopMatrix()

        # RIGHT SMALL BUMP
        glPushMatrix()
        glTranslatef(self.width * 0.38, 0, -self.depth * 0.12)
        glScalef(self.depth / 55, self.depth / 55, self.depth / 55)
        gluSphere(gluNewQuadric(), 20, 10, 10)
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
    def __init__(self, x, y, z, required_key_name=None, callBack=None):
        self.x = x
        self.y = y
        self.z = z
        
        self.width = 50
        self.height = 100
        self.depth = 5
        
        self.required_key_name = required_key_name
        
        if self.required_key_name is None:
            self.locked = False
        else:
            self.locked = True
            
        
        self.angle = 0
        self.closed = True
        self.opening_angle = 0
        self.callBack = callBack
        self.active = True
        self.isLightSource = True
        
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.x, self.y, self.z)
        glTranslatef(-self.width/2, 0, 0)
        glRotate(self.opening_angle, 0, 0, -1)
        
        glTranslatef(self.width/2, 0, 0)
        glColor4f(0.18, 0.17, 0.15, 1)
        glScalef(self.width, 5, self.height)
        glutSolidCube(1)
        glScalef(1/self.width, 1/5, 1/self.height)
        glTranslatef(self.width/2 - 6, 0, 0)
        glColor4f(1, 1, 0, 1)
        glutSolidCube(6)
        glPopMatrix()
        
        distance = getDistance(self.x, self.y, player.x, player.y)
        if distance < self.width:
            if self.locked:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "[LOCKED]")
            elif self.closed:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "Press \'f\'")
    
    def update(self):
        if self.closed:
            if self.opening_angle > 0:
                self.opening_angle -= 100 * dt
        else:
            if self.opening_angle < 90:
                self.opening_angle += 100 * dt
        
    def keyboard_listener(self, key):
        if key == b'f' and self.closed:
            distance = getDistance(self.x, self.y, player.x, player.y)
            if distance < self.width:
                if not self.locked:
                    self.closed = not self.closed
                else:
                    if CHEAT_MODE:
                        self.locked = False
                        self.closed = not self.closed
                    else:
                        for name, color in player.keys:
                            if name == self.required_key_name:
                                self.locked = False
                                self.closed = not self.closed
                                player.keys.remove((self.required_key_name, color))
                                if self.callBack is not None:
                                    if self.required_key_name is not None:
                                        self.callBack()
                
    def collision_detection(self, x, y, radius, collided_with):
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
    def __init__(self, x, y, z, required_key_name=None):
        super().__init__(x, y, z, required_key_name)
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
    
    def collision_detection(self, x, y, radius, collided_with):
        if not self.active:
            return
        min_x = self.x - self.radius
        max_x = self.x + self.radius
        
        min_y = self.y - self.radius
        max_y = self.y + self.radius
        
        if (x + radius > min_x and x - radius < max_x and y + radius > min_y and y - radius < max_y):
            if collided_with == player:
                try:
                    self.callBack()
                except:
                    pass

    def keyboard_listener(self, key):
        pass
    
    def update(self):
        self.rotation += 1

class KEY(ITEM):
    def __init__(self, x, y, color,  name="KEY_X"):
        super().__init__(x, y, 0, 20, 20, 20, 20, color, visible=True, active=True, callback=None, rotation=0, isLightSource=True)
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
    def __init__(self, x, y):
        super().__init__(x, y, 0, 10, 10, 20, 20, (0, 1, 0, 1))
        
    def draw(self):
        if not self.visible:
            return
        r, g, b, a = self.color
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
        if player.health + 15 <= player.max_health:
            player.health += 15

class SHIELD(ITEM):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 10, 10, 20, 20, (0, 0, 1, 1))
        
    def draw(self):
        if not self.visible:
            return
        r, g, b, a = self.color
        glPushMatrix()
        glTranslatef(self.x, self.y, 30)
        glRotatef(self.rotation, 0, 0, 1)
        
        glColor4f(r, g, b, a)
        
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
        if player.shield + 30 <= player.max_shield:
            player.shield += 30


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
        if distance < self.width//2 + player.width//2 and player.z - player.height//2 < 10:
            player.get_damage(self.damage)
            
            theta = math.radians(player.angle)
            fx = math.sin(theta)
            fy = -math.cos(theta)
            
            dx = player.x - self.x
            dy = player.y - self.y
            distance = getDistance(self.x, self.y, player.x, player.y)
            dx = dx/distance
            dy = dy/distance
            
            dot = -(dx * fx + dy * fy)
            if dot < 0:
                player.speed += 50
            else:
                player.speed -= 50

# ENEMY
class ENEMY:
    def __init__(self, x, y, items = []):
        self.x = x
        self.y = y
        self.z = 50
        self.width = 30
        self.depth = 10
        self.height = 50
        self.radius = 30
        
        self.speed = 0
        self.acceleration = 0
        
        
        self.attack_cooldown = 0
        self.attack_cooldown_init = 0.33
        
        self.damage_cooldown = 0
        self.damage_cooldown_init = 0.33
        
        self.shoot_cooldown = 0
        self.shoot_cooldown_init = 1.5
        
        self.detected_player = False
        
        self.init_point = (x, y)
        
        self.angle = 0
        
        self.health = 100
        self.max_health = 100
        
        self.alive = True
        
        self.damage = 20
            
        self.items = items
        
        # type
        #   - attacker
        #   - shooter
        self.type = "attacker"
        
        self.bullets = []
        
    def draw_enemy(self):
        alpha = max(self.health / self.max_health, 0.3)
        
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 0, 0, 1)
        glRotatef(self.angle, 0, 0, 1)
        
        glColor4f(0, 0, 0, alpha)
        
        glutSolidCube(10)
        glPopMatrix()
        
    def draw(self):
        if not self.alive:
            return
        self.draw_enemy()
        
        for bullet in self.bullets:
            bullet.draw()
    
    def attack(self):
        if self.attack_cooldown <= 0:
            player.get_damage(self.damage)
            
            player.speed -= 10
            
            self.attack_cooldown = self.attack_cooldown_init
            
    def fire(self, distance):
        if self.shoot_cooldown <= 0:
            theta = math.radians(self.angle)
            fx = math.sin(theta)
            fy = -math.cos(theta)
            
            dx = (player.x - self.x) / distance
            dy = (player.y - self.y) / distance
            
            dot = fx * dx + fy * dy
            if abs(dot + 1) < 0.2:
                self.bullets.append(BULLET(self.x, self.y, self.height/2, -fx, -fy, self))
            
            self.shoot_cooldown = self.shoot_cooldown_init
        
    def face_toward_player(self):
        if self.detected_player:
            px = player.x
            py = player.y

        else:
            px = self.init_point[0]
            py = self.init_point[1]
        
        dx = px - self.x
        dy = py - self.y
        dx *= -1

        target_angle = math.degrees(math.atan2(dx, dy))

        difference = (target_angle - self.angle + 180) % 360 - 180
        
        rotation_speed = 120 * dt

        if difference > rotation_speed:
            self.angle += rotation_speed

        elif difference < -rotation_speed:
            self.angle -= rotation_speed

        else:
            self.angle = target_angle
            return True
        
        self.angle = self.angle % 360

        return False
    
    def get_damage(self, damage):
        self.health -= damage
    
    def get_attacked(self, distance):
        
        if distance >= self.radius + player.radius:
            return
        
        if self.damage_cooldown > 0:
            return
        
        ptheta = math.radians(player.angle)

        pfx = math.sin(ptheta)
        pfy = -math.cos(ptheta)
        
        dx = player.x - self.x
        dy = player.y - self.y
        
        if distance <= 0.001:
            return
        
        dx = dx/distance
        dy = dy/distance
        dot = dx * pfx + dy * pfy
            
        if abs(1 + dot) < 0.2:
            self.get_damage(30)
            self.speed -= 30
            self.damage_cooldown = self.damage_cooldown_init
    
    def update_health(self):
        if self.health <= 0:
            r = random.random()
            
            self.alive = False
            
            if r > 0.3:
                item_list.append(random.choice([HEALTH(self.x, self.y), SHIELD(self.x, self.y)]))
                
            
            for item in self.items:
                item.x = self.x
                item.y = self.y
                item.z = self.z
                item_list.append(item)
    
    def collision_detection(self, new_x, new_y):
        # CHECK COLLISION WITH WALL AND OBJECTS
        move_x = True
        move_y = True
        for room in room_list:

            if not move_x and not move_y:
                break

            if move_x:
                if room.collision_detection(new_x, self.y, 10):
                    move_x = False

            if move_y:
                if room.collision_detection(self.x, new_y, 10):
                    move_y = False
                    
        for item in item_list:
            if not move_x and not move_y:
                break

            if move_x:
                if item.collision_detection(new_x, self.y, 10, self):
                    move_x = False

            if move_y:
                if item.collision_detection(self.x, new_y, 10, self):
                    move_y = False
        
        return move_x, move_y
    
    def update(self):
        if not self.alive:
            return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        
        self.update_health()
        
        if not self.alive:
            return
        
        distance = getDistance(self.x, self.y, player.x, player.y)
        
        if distance < 400:
            self.detected_player = True
        else:
            self.detected_player = False
        
        # Choose wheather go behind player or initial point
        if self.detected_player:
            dx = player.x - self.x
            dy = player.y - self.y
        else:
            dx = self.init_point[0] - self.x
            dy = self.init_point[1] - self.y
            
        # FACING TOWARD PLAYER
        facing_target = self.face_toward_player()
        
        if self.detected_player:
            collision_radius = self.radius + 10
            
            if facing_target and self.type == "shooter" and 100 > distance:
                self.fire(distance)
                        
            elif distance < collision_radius and  self.type == "attacker":
                self.attack()
                
            if player.attack_on:
                self.get_attacked(distance)
            
        new_x = self.x + dx * self.speed * dt
        new_y = self.y + dy * self.speed * dt
        
        
        move_x, move_y = self.collision_detection(new_x, new_y)
                    
        # move_x = False
        # move_y = False
        
        # MOVE
        if distance > 30 and facing_target:

            if move_x:
                self.x = new_x

            if move_y:
                self.y = new_y
                
        for bullet in self.bullets:
            bullet.update()
            
        self.speed += (self.acceleration + ROOM_LEVEL * 10) * dt
        self.speed *= pow(0.5, dt * 60)

class DOG(ENEMY):
    def __init__(self, x, y, items=[]):
        super().__init__(x, y, items)
        
        self.health = 70
        self.max_health = 70
        
        # self.type = 'shooter'
        
        self.transmission_cooldown = 0
        self.transmission_cooldown_init = 2.5
    
    def draw_enemy(self):
        if self.health <= 0:
            return

        alpha = max(0.4, (self.health/self.max_health))
        
        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 0, 0, 1)
        glRotatef(self.angle, 0, 0, 1)
        
        glScalef(1, 5, 1)

        # MAIN BODY
        glPushMatrix()

        glColor4f(0.18, 0.08, 0.12, alpha)

        glScalef(
            self.width * 1.15,
            self.depth * 0.75,
            self.height * 0.55
        )

        gluSphere(gluNewQuadric(), 0.5, 16, 16)

        glPopMatrix()

        # HEAD
        glPushMatrix()

        glTranslatef(
            0,
            -self.depth * 0.35,
            self.height * 0.20
        )

        glColor4f(0.30, 0.12, 0.16, alpha)

        glScalef(
            self.width * 0.75,
            self.depth * 0.65,
            self.height * 0.55
        )

        gluSphere(gluNewQuadric(), 0.5, 16, 16)

        glPopMatrix()

        # LEFT HORN
        glPushMatrix()

        glTranslatef(
            -self.width * 0.32,
            -self.depth * 0.25,
            self.height * 0.55
        )

        glRotatef(-20, 0, 1, 0)

        glColor4f(0.08, 0.06, 0.05, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.18,
            self.height * 0.55
        )

        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 12, 4)
        

        glPopMatrix()

        # RIGHT HORN
        glPushMatrix()

        glTranslatef(
            self.width * 0.32,
            -self.depth * 0.25,
            self.height * 0.55
        )

        glRotatef(20, 0, 1, 0)

        glColor4f(0.08, 0.06, 0.05, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.18,
            self.height * 0.55
        )

        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 12, 4)

        glPopMatrix()

        # LEFT EYE SOCKET
        glPushMatrix()

        glTranslatef(
            -self.width * 0.22,
            -self.depth * 0.61,
            self.height * 0.27
        )

        glColor4f(0.03, 0.01, 0.01, alpha)

        glScalef(
            self.width * 0.20,
            self.depth * 0.08,
            self.height * 0.15
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # LEFT GLOWING EYE
        glPushMatrix()

        glTranslatef(
            -self.width * 0.22,
            -self.depth * 0.67,
            self.height * 0.27
        )

        glColor4f(1.0, 0.15, 0.02, alpha)

        glScalef(
            self.width * 0.09,
            self.depth * 0.04,
            self.height * 0.07
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # RIGHT EYE SOCKET
        glPushMatrix()

        glTranslatef(
            self.width * 0.22,
            -self.depth * 0.61,
            self.height * 0.27
        )

        glColor4f(0.03, 0.01, 0.01, alpha)

        glScalef(
            self.width * 0.20,
            self.depth * 0.08,
            self.height * 0.15
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # RIGHT GLOWING EYE
        glPushMatrix()

        glTranslatef(
            self.width * 0.22,
            -self.depth * 0.67,
            self.height * 0.27
        )

        glColor4f(1.0, 0.15, 0.02, alpha)

        glScalef(
            self.width * 0.09,
            self.depth * 0.04,
            self.height * 0.07
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # MOUTH
        glPushMatrix()

        glTranslatef(
            0,
            -self.depth * 0.66,
            self.height * 0.05
        )

        glColor4f(0.02, 0.01, 0.01, alpha)

        glScalef(
            self.width * 0.48,
            self.depth * 0.08,
            self.height * 0.18
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # TEETH
        for x in [-0.16, -0.08, 0.0, 0.08, 0.16]:

            glPushMatrix()

            glTranslatef(
                self.width * x,
                -self.depth * 0.71,
                self.height * 0.09
            )

            glColor4f(0.9, 0.8, 0.55, alpha)

            glScalef(
                self.width * 0.055,
                self.depth * 0.035,
                self.height * 0.13
            )

            gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 8, 3)

            glPopMatrix()

        # FRONT LEFT LEG
        glPushMatrix()

        glTranslatef(
            -self.width * 0.45,
            -self.depth * 0.25,
            -self.height * 0.30
        )

        glRotatef(-12, 0, 1, 0)

        glColor4f(0.12, 0.06, 0.08, alpha)

        glScalef(
            self.width * 0.28,
            self.depth * 0.30,
            self.height * 0.65
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # FRONT RIGHT LEG
        glPushMatrix()

        glTranslatef(
            self.width * 0.45,
            -self.depth * 0.25,
            -self.height * 0.30
        )

        glRotatef(12, 0, 1, 0)

        glColor4f(0.12, 0.06, 0.08, alpha)

        glScalef(
            self.width * 0.28,
            self.depth * 0.30,
            self.height * 0.65
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # BACK LEFT LEG
        glPushMatrix()

        glTranslatef(
            -self.width * 0.40,
            self.depth * 0.25,
            -self.height * 0.30
        )

        glRotatef(-18, 0, 1, 0)

        glColor4f(0.10, 0.05, 0.07, alpha)

        glScalef(
            self.width * 0.25,
            self.depth * 0.28,
            self.height * 0.60
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # BACK RIGHT LEG
        glPushMatrix()

        glTranslatef(
            self.width * 0.40,
            self.depth * 0.25,
            -self.height * 0.30
        )

        glRotatef(18, 0, 1, 0)

        glColor4f(0.10, 0.05, 0.07, alpha)

        glScalef(
            self.width * 0.25,
            self.depth * 0.28,
            self.height * 0.60
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)

        glPopMatrix()

        # CLAW - LEFT
        glPushMatrix()

        glTranslatef(
            -self.width * 0.48,
            -self.depth * 0.38,
            -self.height * 0.58
        )

        glColor4f(0.75, 0.65, 0.45, alpha)

        glScalef(
            self.width * 0.15,
            self.depth * 0.15,
            self.height * 0.25
        )

        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 8, 3)

        glPopMatrix()

        # CLAW - RIGHT
        glPushMatrix()

        glTranslatef(
            self.width * 0.48,
            -self.depth * 0.38,
            -self.height * 0.58
        )

        glColor4f(0.75, 0.65, 0.45, alpha)

        glScalef(
            self.width * 0.15,
            self.depth * 0.15,
            self.height * 0.25
        )

        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 8, 3)

        glPopMatrix()

        # TAIL
        glPushMatrix()

        glTranslatef(
            0,
            self.depth * 0.58,
            self.height * 0.05
        )

        glRotatef(-35, 1, 0, 0)

        glColor4f(0.16, 0.07, 0.10, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.65,
            self.height * 0.18
        )

        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 12, 4)

        glPopMatrix()

        glPopMatrix()

    def update(self):
        super().update()
        if self.transmission_cooldown > 0:
            self.transmission_cooldown -= dt
            if self.transmission_cooldown < 0:
                self.transmission_cooldown = 0
        
        if self.detected_player and self.transmission_cooldown == 0:
            if random.random()*10 < 0.3:
                theta = math.radians(player.angle)
                x = player.x - math.sin(theta) * 80
                y = player.y + math.cos(theta) * 80
                self.x = x
                self.y = y
                self.angle = (self.angle + 180)%360
                self.transmission_cooldown = self.transmission_cooldown_init

class ZOMBIE(ENEMY):
    def __init__(self, x, y, items=[]):
        super().__init__(x, y, items)
        
    def draw_enemy(self):
        if self.health <= 0:
            return

        glPushMatrix()

        glTranslatef(self.x, self.y, self.z)
        glRotatef(180, 0, 0, 1)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(1, 3, 1)
        # TORSO
        glPushMatrix()
        glColor4f(0.10, 0.28, 0.12, max(0.5, self.health/100))
        glScalef(self.width * 0.95,
                self.depth * 0.65,
                self.height * 0.70)
        glutSolidCube(1)
        glPopMatrix()

        # CHEST / SHIRT FRONT
        glPushMatrix()
        glTranslatef(0, -self.depth * 0.34, self.height * 0.02)

        glColor4f(0.16, 0.38, 0.18, max(0.5, self.health/100))
        glScalef(self.width * 0.65,
                0.05,
                self.height * 0.48)
        glutSolidCube(1)
        glPopMatrix()

        # HEAD
        glPushMatrix()
        glTranslatef(0, 0, self.height * 0.55)

        glColor4f(0.30, 0.62, 0.30, max(0.5, self.health/100))

        glScalef(self.width * 0.72,
                self.depth * 0.75,
                self.height * 0.48)

        gluSphere(gluNewQuadric(), 0.5, 16, 16)
        glPopMatrix()

        # LEFT EAR
        glPushMatrix()
        glTranslatef(
            -self.width * 0.38,
            0,
            self.height * 0.55
        )

        glColor4f(0.25, 0.52, 0.25, max(0.5, self.health/100))

        glScalef(
            self.width * 0.16,
            self.depth * 0.30,
            self.height * 0.18
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # RIGHT EAR
        glPushMatrix()
        glTranslatef(
            self.width * 0.38,
            0,
            self.height * 0.55
        )

        glColor4f(0.25, 0.52, 0.25, max(0.5, self.health/100))

        glScalef(
            self.width * 0.16,
            self.depth * 0.30,
            self.height * 0.18
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # LEFT EYE
        glPushMatrix()
        glTranslatef(
            -self.width * 0.20,
            -self.depth * 0.34,
            self.height * 0.61
        )

        # Eye socket
        glColor4f(0.05, 0.08, 0.04, max(0.5, self.health/100))

        glScalef(
            self.width * 0.20,
            self.depth * 0.08,
            self.height * 0.14
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # Red eye
        glPushMatrix()
        glTranslatef(
            -self.width * 0.20,
            -self.depth * 0.40,
            self.height * 0.61
        )

        glColor4f(1.0, 0.02, 0.02, max(0.5, self.health/100))

        glScalef(
            self.width * 0.09,
            self.depth * 0.04,
            self.height * 0.07
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # RIGHT EYE
        glPushMatrix()
        glTranslatef(
            self.width * 0.20,
            -self.depth * 0.34,
            self.height * 0.61
        )

        glColor4f(0.05, 0.08, 0.04, max(0.5, self.health/100))

        glScalef(
            self.width * 0.20,
            self.depth * 0.08,
            self.height * 0.14
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # Red eye
        glPushMatrix()
        glTranslatef(
            self.width * 0.20,
            -self.depth * 0.40,
            self.height * 0.61
        )

        glColor4f(1.0, 0.02, 0.02, max(0.5, self.health/100))

        glScalef(
            self.width * 0.09,
            self.depth * 0.04,
            self.height * 0.07
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # NOSE
        glPushMatrix()
        glTranslatef(
            0,
            -self.depth * 0.39,
            self.height * 0.50
        )

        glColor4f(0.20, 0.45, 0.20, max(0.5, self.health/100))

        glScalef(
            self.width * 0.12,
            self.depth * 0.10,
            self.height * 0.15
        )
        
        gluCylinder(gluNewQuadric(), 0.5, 0, 1.0, 10, 4)
        glPopMatrix()

        # MOUTH
        glPushMatrix()
        glTranslatef(
            0,
            -self.depth * 0.39,
            self.height * 0.39
        )

        glColor4f(0.03, 0.01, 0.01, max(0.5, self.health/100))

        glScalef(
            self.width * 0.42,
            self.depth * 0.06,
            self.height * 0.13
        )

        glutSolidCube(1)
        glPopMatrix()

        # TEETH - TOP
        for x in [-0.13, -0.04, 0.05, 0.14]:
            glPushMatrix()

            glTranslatef(
                self.width * x,
                -self.depth * 0.44,
                self.height * 0.43
            )

            glColor4f(0.85, 0.82, 0.65, max(0.5, self.health/100))

            glScalef(
                self.width * 0.06,
                self.depth * 0.035,
                self.height * 0.08
            )

            glutSolidCube(1)
            glPopMatrix()

        # LEFT ARM
        glPushMatrix()

        glTranslatef(
            self.width * 0.63,
            0,
            self.height * 0.08
        )

        glRotatef(-25, 0, 1, 0)

        glColor4f(0.25, 0.55, 0.25, max(0.5, self.health/100))

        glScalef(
            self.width * 0.30,
            self.depth * 0.55,
            self.height * 0.58
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # RIGHT ARM
        glPushMatrix()

        glTranslatef(
            -self.width * 0.63,
            0,
            self.height * 0.08
        )

        glRotatef(25, 0, 1, 0)

        glColor4f(0.25, 0.55, 0.25, max(0.5, self.health/100))

        glScalef(
            self.width * 0.30,
            self.depth * 0.55,
            self.height * 0.58
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        # LEFT LEG
        glPushMatrix()

        glTranslatef(
            -self.width * 0.23,
            0,
            -self.height * 0.55
        )

        glColor4f(0.07, 0.09, 0.12, max(0.5, self.health/100))

        glScalef(
            self.width * 0.38,
            self.depth * 0.55,
            self.height * 0.50
        )

        glutSolidCube(1)
        glPopMatrix()

        # RIGHT LEG
        glPushMatrix()

        glTranslatef(
            self.width * 0.23,
            0,
            -self.height * 0.55
        )

        glColor4f(0.07, 0.09, 0.12, max(0.5, self.health/100))

        glScalef(
            self.width * 0.38,
            self.depth * 0.55,
            self.height * 0.50
        )

        glutSolidCube(1)
        glPopMatrix()

        # LEFT BOOT
        glPushMatrix()

        glTranslatef(
            -self.width * 0.23,
            -self.depth * 0.05,
            -self.height * 0.82
        )

        glColor4f(0.04, 0.04, 0.04, max(0.5, self.health/100))

        glScalef(
            self.width * 0.45,
            self.depth * 0.75,
            self.height * 0.18
        )

        glutSolidCube(1)
        glPopMatrix()

        # RIGHT BOOT
        glPushMatrix()

        glTranslatef(
            self.width * 0.23,
            -self.depth * 0.05,
            -self.height * 0.82
        )

        glColor4f(0.04, 0.04, 0.04, max(0.5, self.health/100))

        glScalef(
            self.width * 0.45,
            self.depth * 0.75,
            self.height * 0.18
        )

        glutSolidCube(1)
        glPopMatrix()

        # HAIR
        glPushMatrix()

        glTranslatef(
            0,
            0,
            self.height * 0.78
        )

        glColor4f(0.03, 0.03, 0.03, max(0.5, self.health/100))

        glScalef(
            self.width * 0.70,
            self.depth * 0.70,
            self.height * 0.12
        )

        gluSphere(gluNewQuadric(), 0.5, 12, 12)
        glPopMatrix()

        glPopMatrix()

class SKELETON(ENEMY):
    def __init__(self, x, y, items=[]):
        super().__init__(x, y, items)
        self.type = 'shooter'
        self.quadric = gluNewQuadric()

    def draw_enemy(self):
        if self.health <= 0:
            return

        glPushMatrix()

        glTranslatef(self.x, self.y, 20)
        glRotatef(180, 0, 0, 1)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(1, 3, 1)

        alpha = max(0.5, self.health / 100)

        bone = (0.78, 0.75, 0.64)

        # HEAD
        glPushMatrix()

        glTranslatef(0, 0, self.height * 0.58)

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.70,
            self.depth * 0.75,
            self.height * 0.42
        )

        gluSphere(self.quadric, 0.5, 16, 12)

        glPopMatrix()

        # LEFT EYE SOCKET
        glPushMatrix()

        glTranslatef(
            -self.width * 0.20,
            -self.depth * 0.34,
            self.height * 0.62
        )

        glColor4f(0.02, 0.02, 0.02, alpha)

        glScalef(
            self.width * 0.17,
            self.depth * 0.08,
            self.height * 0.12
        )

        gluSphere(self.quadric, 0.5, 10, 8)

        glPopMatrix()

        # RIGHT EYE SOCKET
        glPushMatrix()

        glTranslatef(
            self.width * 0.20,
            -self.depth * 0.34,
            self.height * 0.62
        )

        glColor4f(0.02, 0.02, 0.02, alpha)

        glScalef(
            self.width * 0.17,
            self.depth * 0.08,
            self.height * 0.12
        )

        gluSphere(self.quadric, 0.5, 10, 8)

        glPopMatrix()

        # NOSE
        glPushMatrix()

        glTranslatef(
            0,
            -self.depth * 0.36,
            self.height * 0.52
        )

        glColor4f(0.02, 0.02, 0.02, alpha)

        glScalef(
            self.width * 0.10,
            self.depth * 0.06,
            self.height * 0.10
        )

        gluCylinder(
            self.quadric,
            0.08,
            0.02,
            0.15,
            8,
            4
        )

        glPopMatrix()

        # JAW
        glPushMatrix()

        glTranslatef(
            0,
            -self.depth * 0.02,
            self.height * 0.40
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.48,
            self.depth * 0.38,
            self.height * 0.10
        )

        glutSolidCube(1)

        glPopMatrix()

        # TEETH
        for x in [-0.14, -0.07, 0, 0.07, 0.14]:

            glPushMatrix()

            glTranslatef(
                self.width * x,
                -self.depth * 0.22,
                self.height * 0.42
            )

            glColor4f(0.90, 0.87, 0.72, alpha)

            glScalef(
                self.width * 0.045,
                self.depth * 0.04,
                self.height * 0.065
            )

            glutSolidCube(1)

            glPopMatrix()

        # NECK
        glPushMatrix()

        glTranslatef(
            0,
            0,
            self.height * 0.30
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.18,
            self.height * 0.15
        )

        gluCylinder(
            self.quadric,
            0.5,
            0.5,
            1.0,
            8,
            4
        )

        glPopMatrix()

        # SPINE
        glColor4f(*bone, alpha)

        for i in range(5):

            glPushMatrix()

            glTranslatef(
                0,
                0,
                self.height * (0.23 - i * 0.085)
            )

            gluSphere(
                self.quadric,
                self.width * 0.13,
                8,
                6
            )

            glPopMatrix()

        # RIBCAGE
        # Torus is replaced by pairs of curved-looking
        # cylinder segments.
        for z_offset, scale in [
            (0.22, 1.0),
            (0.15, 0.9),
            (0.08, 0.78)
        ]:

            # -------------------------
            # LEFT RIB
            # -------------------------
            glPushMatrix()

            glTranslatef(
                -self.width * 0.20 * scale,
                0,
                self.height * z_offset
            )

            glRotatef(70, 1, 0, 0)
            glRotatef(-25, 0, 1, 0)

            glColor4f(*bone, alpha)

            glScalef(
                self.width * 0.10 * scale,
                self.depth * 0.08,
                self.height * 0.25
            )

            gluCylinder(
                self.quadric,
                0.5,
                0.5,
                1.0,
                8,
                4
            )

            glPopMatrix()

            # -------------------------
            # RIGHT RIB
            # -------------------------
            glPushMatrix()

            glTranslatef(
                self.width * 0.20 * scale,
                0,
                self.height * z_offset
            )

            glRotatef(70, 1, 0, 0)
            glRotatef(25, 0, 1, 0)

            glColor4f(*bone, alpha)

            glScalef(
                self.width * 0.10 * scale,
                self.depth * 0.08,
                self.height * 0.25
            )

            gluCylinder(
                self.quadric,
                0.5,
                0.5,
                1.0,
                8,
                4
            )

            glPopMatrix()

        # LEFT ARM
        glPushMatrix()

        glTranslatef(
            self.width * 0.42,
            0,
            self.height * 0.20
        )

        glRotatef(-12, 0, 1, 0)

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.12,
            self.depth * 0.12,
            self.height * 0.42
        )

        gluCylinder(
            self.quadric,
            0.5,
            0.5,
            1.0,
            8,
            4
        )

        glPopMatrix()

        # LEFT HAND
        glPushMatrix()

        glTranslatef(
            self.width * 0.43,
            0,
            -self.height * 0.05
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.18,
            self.height * 0.10
        )

        gluSphere(self.quadric, 0.5, 8, 6)

        glPopMatrix()

        # RIGHT ARM
        glPushMatrix()

        glTranslatef(
            -self.width * 0.42,
            0,
            self.height * 0.20
        )

        glRotatef(12, 0, 1, 0)

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.12,
            self.depth * 0.12,
            self.height * 0.42
        )

        gluCylinder(
            self.quadric,
            0.5,
            0.5,
            1.0,
            8,
            4
        )

        glPopMatrix()

        # RIGHT HAND
        glPushMatrix()

        glTranslatef(
            -self.width * 0.43,
            0,
            -self.height * 0.05
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.18,
            self.depth * 0.18,
            self.height * 0.10
        )

        gluSphere(self.quadric, 0.5, 8, 6)

        glPopMatrix()

        # LEFT LEG
        glPushMatrix()

        glTranslatef(
            -self.width * 0.18,
            0,
            -self.height * 0.25
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.13,
            self.depth * 0.13,
            self.height * 0.55
        )

        gluCylinder(
            self.quadric,
            0.5,
            0.5,
            1.0,
            8,
            4
        )

        glPopMatrix()

        # RIGHT LEG
        glPushMatrix()

        glTranslatef(
            self.width * 0.18,
            0,
            -self.height * 0.25
        )

        glColor4f(*bone, alpha)

        glScalef(
            self.width * 0.13,
            self.depth * 0.13,
            self.height * 0.55
        )

        gluCylinder(
            self.quadric,
            0.5,
            0.5,
            1.0,
            8,
            4
        )

        glPopMatrix()

        # FEET
        for x in [-0.18, 0.18]:

            glPushMatrix()

            glTranslatef(
                self.width * x,
                -self.depth * 0.10,
                -self.height * 0.55
            )

            glColor4f(*bone, alpha)

            glScalef(
                self.width * 0.22,
                self.depth * 0.35,
                self.height * 0.08
            )

            glutSolidCube(1)

            glPopMatrix()

        glPopMatrix()


def create_world():
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
    }
    return world

WORLD = create_world()

# Callbacks
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    
    global GAME_STATE, CHEAT_MODE, VIEW_MODE, PAUSE
    if GAME_STATE == "GAME":
        if key == b'p':
            PAUSE = not PAUSE
        if PAUSE:
            return
        if key == b'w':
            player.move(1)
        if key == b's':
            player.move(-1)
        if key == b'a':
            player.rotate(1)
        if key == b'd':
            player.rotate(-1)
            
        if key == b'z':
            if player.shield > 0:
                player.shield_on = not player.shield_on
            
        if key == b'v':
            VIEW_MODE = (VIEW_MODE + 1) % 4
            
        if key == b'c':
            CHEAT_MODE = not CHEAT_MODE
            
        if key == b' ':
            print(room_to_move.x, room_to_move.y)
            player.jump()
        
        for item in item_list:
            item.keyboard_listener(key)

        if key == b'\x1b':
            GAME_STATE = "MENU"
            
    elif GAME_STATE == "ROOM SELECT":
        if key == b'\x1b':
            GAME_STATE = "MENU"
            
    elif GAME_STATE == "MENU":
        if key == b'\x1b':
            glutLeaveMainLoop()

def specialKeyListener(key, x, y):
    # Move camera up (UP arrow key)
    if GAME_STATE == "GAME":
        if PAUSE:
            return
        if key == GLUT_KEY_UP:
            pass
            
        # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN:
            pass
            
        # moving camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            pass

        # moving camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            pass
        
        if key == 112: # Left Shift
            player.sprint = not player.sprint

def mouseListener(button, state, x, y):
    global GAME_STATE
    
    x, y = convert_coordinate(x, y)
    
    if GAME_STATE == "MENU":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            start_button.click(x, y, start_button_callback)
            help_button.click(x,y,help_button_callback)
            exit_button.click(x,y, glutLeaveMainLoop)

    elif GAME_STATE == "ROOM SELECT":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            for i in WORLD:
                button = WORLD[i]["button"]
                GAME_STATE = "GAME"
                button.click(x, y, game_init, i)
            
    elif GAME_STATE == "HELP":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            help_back_button.click(x, y, help_back_button_callback)
            
    elif GAME_STATE == "GAME":
        if PAUSE:
            return
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            player.attack()
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            player.fire()
        if button == 3:
            camera.target_up += 1
        if button == 4:
            camera.target_up -= 1

    elif GAME_STATE == "ESCAPED":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            main_menu_button.click(x, y, main_menu_button_callback)
    
    elif GAME_STATE == "GAMEOVER":
        if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            main_menu_button.click(x, y, main_menu_button_callback)

def idle(value=0):
    global last_time, dt, SECONDS
    
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    dt = min(dt, 1/60)
    
    if GAME_STATE == 'GAME':
        if PAUSE:
            return
        SECONDS += dt
        player.update()
        camera.update()
        hud.update()
        
        for room in room_list:
            distance = getDistance(room.x, room.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                room.update()
        
        for item in item_list:
            distance = getDistance(item.x, item.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                item.update()
            
        for item in static_item_list:
            distance = getDistance(item.x, item.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                item.update()
            
        for arrow in hint_arrow_list:
            distance = getDistance(arrow.x, arrow.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                arrow.update()
            
        for trap in trap_list:
            distance = getDistance(trap.x, trap.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                trap.update()
            
        for enemy in enemy_list:
            distance = getDistance(enemy.x, enemy.y, player.x, player.y)
            if distance < DRAWING_RADIUS:
                if enemy.alive:
                    enemy.update()
                else:
                    enemy_list.remove(enemy)
        
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
    GAME_STATE = "ROOM SELECT"
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

player = None
hud = None

def game_init(room_no):
    global item_list, static_item_list, room_list, room_to_move, player, hud, enemy_list, trap_list, hint_arrow_list, CHEAT_MODE, SECONDS, ROOM_LEVEL
    CHEAT_MODE = False 
    SECONDS = 0
    ROOM_LEVEL = 1
    
    WORLD = create_world()
    room = WORLD[room_no]
    
    px, py = room["spawn_point"]
    # px, py = (-1100, -2280)
    player = ADVENTURER(px, py)
    hud = HUD()
    
    entities = room["entities"]
    room_list = entities["room_list"]
    item_list = entities["item_list"]
    trap_list = entities["trap_list"]
    static_item_list = entities['static_item_list']
    hint_arrow_list = entities['hint_arrow_list']
    enemy_list = entities['enemy_list']
    
    room_to_move = hint_arrow_list[-1]
 
game_init("1")

# Drawing Function
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
        if distance < DRAWING_RADIUS:
            item.draw()
        
    for item in static_item_list:
        distance = math.sqrt((player.x - item.x)**2 + (player.y - item.y)**2)
        if distance < DRAWING_RADIUS:
            item.draw()
            
    for item in hint_arrow_list:
        distance = math.sqrt((player.x - item.x)**2 + (player.y - item.y)**2)
        if distance < DRAWING_RADIUS and CHEAT_MODE:
            item.draw()
        
    for trap in trap_list:
        distance = math.sqrt((player.x - trap.x)**2 + (player.y - trap.y)**2)
        if distance < DRAWING_RADIUS:
            trap.draw()
        
    for enemy in enemy_list:
        distance = math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2)
        if distance < DRAWING_RADIUS:
            enemy.draw()
        
    player.draw()
    hud.draw()
    camera.draw()

def draw_escaped():
    global SECONDS
    glColor4f(1, 0, 0, 1)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    end_quote = "A NEW LIFE BEGINS"
    draw_text(-6*len(end_quote), 140, end_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
    s = int(SECONDS)
    m = int(s/60)
    s = int(s%60)
    if s < 10:
        time_quote = f"Time: {m}:0{s}"
    else:
        time_quote = f"Time: {m}:{s}"
    draw_text(-6*len(time_quote), 110, time_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
    main_menu_button.draw()
    
def draw_game_over():
    glColor4f(1, 0, 0, 1)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    end_quote = "GAME OVER!"
    draw_text(-6*len(end_quote), 100, end_quote, font=GLUT_BITMAP_TIMES_ROMAN_24)
    main_menu_button.draw()
    
def draw_room_select():
    glColor4f(1, 0, 0, 1)
    draw_rect(0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    draw_text(-100, WINDOW_SIZE[1]//2 - 100, "SELECT WORLD", font=GLUT_BITMAP_TIMES_ROMAN_24)
    
    for i in WORLD:
        WORLD[i]['button'].draw()

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
    elif GAME_STATE == "ROOM SELECT":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_room_select()
    elif GAME_STATE == "GAME":
        glEnable(GL_DEPTH_TEST)
        setupCamera()
        draw_game()
    elif GAME_STATE == "ESCAPED":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_escaped()
    elif GAME_STATE == "GAMEOVER":
        glDisable(GL_DEPTH_TEST)
        setup_projection()
        draw_game_over()
        
    
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
