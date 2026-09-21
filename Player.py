from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random

from Utilities import *

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
        self.z += self.speedZ * global_vars.dt
        self.speedZ -= 700 * global_vars.dt
        
        if self.z <= self.height / 2:
            self.z = self.height / 2
            self.speedZ = 0
            self.on_air = False

        if self.on_air and self.speed != 0:
            direction = self.speed / abs(self.speed)
            self.move(0.45 * direction * global_vars.dt * 60)
    
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

            self.attack_angle -= 600 * global_vars.dt

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
        if global_vars.CHEAT_MODE:
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
        self.speed += acc * global_vars.dt * direction
    
    def rotate(self, direction):
        self.rotation_direction = direction
        self.rotating = True  

    def move_body(self):
        self.arm_angle += abs(self.speed) * global_vars.dt * self.body_angle_direction
        
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
        dx = dx * self.speed * global_vars.dt
        dy = dy * self.speed * global_vars.dt
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        move_x = True
        move_y = True
        
        for room in global_vars.room_list:
            move_x = (move_x and not room.collision_detection(new_x, self.y, 15))
            move_y = (move_y and not room.collision_detection(self.x, new_y, 15))
        
        for item in global_vars.item_list:
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

    def mouseListener(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.attack()
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            self.fire()

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
        self.x += self.direction_x * global_vars.dt * self.speed
        self.y += self.direction_y * global_vars.dt * self.speed
        
        for enemy in global_vars.enemy_list:
            if enemy == self.owner:
                continue
            distance = getDistance(self.x, self.y, enemy.x, enemy.y)
            if distance <= enemy.radius:
                self.active = False
                enemy.get_damage(30)
                
        
        for room in global_vars.room_list:
            collided = room.collision_detection(self.x, self.y, 5)
            if collided:
                self.active = False
