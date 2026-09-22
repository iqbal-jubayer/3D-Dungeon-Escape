from Item import HEALTH, SHIELD
from Player import BULLET
from Utilities import *

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
        
        self.sound_a = 0
        
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
            global_vars.player.get_damage(self.damage)
            
            global_vars.player.speed -= 10
            
            self.attack_cooldown = self.attack_cooldown_init
            
    def fire(self, distance):
        if self.shoot_cooldown <= 0:
            theta = math.radians(self.angle)
            fx = math.sin(theta)
            fy = -math.cos(theta)
            
            dx = (global_vars.player.x - self.x) / distance
            dy = (global_vars.player.y - self.y) / distance
            
            dot = fx * dx + fy * dy
            if abs(dot + 1) < 0.2:
                self.bullets.append(BULLET(self.x, self.y, self.height/2, -fx, -fy, self))
            
            self.shoot_cooldown = self.shoot_cooldown_init
        
    def face_toward_player(self):
        if self.detected_player:
            px = global_vars.player.x
            py = global_vars.player.y

        else:
            px = self.init_point[0]
            py = self.init_point[1]
        
        dx = px - self.x
        dy = py - self.y
        dx *= -1

        target_angle = math.degrees(math.atan2(dx, dy))

        difference = (target_angle - self.angle + 180) % 360 - 180
        
        rotation_speed = 120 * global_vars.dt

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
        
        if distance >= self.radius + global_vars.player.radius:
            return
        
        if self.damage_cooldown > 0:
            return
        
        ptheta = math.radians(global_vars.player.angle)

        pfx = math.sin(ptheta)
        pfy = -math.cos(ptheta)
        
        dx = global_vars.player.x - self.x
        dy = global_vars.player.y - self.y
        
        if distance <= 0.001:
            return
        
        dx = dx/distance
        dy = dy/distance
        dot = dx * pfx + dy * pfy
            
        if abs(1 + dot) < 0.2:
            self.get_damage(30)
            self.speed -= 10
            self.damage_cooldown = self.damage_cooldown_init
    
    def update_health(self):
        if self.health <= 0:
            r = random.random()
            
            self.alive = False
            
            if r > 0.3:
                global_vars.item_list.append(random.choice([HEALTH(self.x, self.y), SHIELD(self.x, self.y)]))
                
            
            for item in self.items:
                item.x = self.x
                item.y = self.y
                item.z = self.z
                global_vars.item_list.append(item)
    
    def collision_detection(self, new_x, new_y):
        # CHECK COLLISION WITH WALL AND OBJECTS
        move_x = True
        move_y = True
        for room in global_vars.room_list:

            if not move_x and not move_y:
                break

            if move_x:
                if room.collision_detection(new_x, self.y, 10):
                    move_x = False

            if move_y:
                if room.collision_detection(self.x, new_y, 10):
                    move_y = False
                    
        for item in global_vars.item_list:
            if not move_x and not move_y:
                break

            if move_x:
                if item.collision_detection(new_x, self.y, 10, self):
                    move_x = False

            if move_y:
                if item.collision_detection(self.x, new_y, 10, self):
                    move_y = False
        
        return move_x, move_y
    
    def make_sound(self):
        if not global_vars.enemy_sound_channel.get_busy() and global_vars.enemy_sound_timer >= global_vars.enemy_sound_time_delay:
            snd = random.choice(global_vars.enemy_sound_list)
            if global_vars.enemy_sound_last is None:
                global_vars.enemy_sound_last = snd
            else:
                while snd == global_vars.enemy_sound_last:
                    snd = random.choice(global_vars.enemy_sound_list)
                global_vars.enemy_sound_last = snd
            global_vars.enemy_sound_channel.play(snd)
            global_vars.enemy_sound_timer = 0
        
        if not global_vars.enemy_sound_channel.get_busy():
            global_vars.enemy_sound_timer += global_vars.dt
    
    def update(self):
        if not self.alive:
            return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= global_vars.dt
        
        if self.damage_cooldown > 0:
            self.damage_cooldown -= global_vars.dt
            
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= global_vars.dt
        
        self.update_health()
        
        if not self.alive:
            return
        
        distance = getDistance(self.x, self.y, global_vars.player.x, global_vars.player.y)
        
        if distance < 400:
            self.detected_player = True
            self.make_sound()
        else:
            self.detected_player = False
        
        # Choose wheather go behind player or initial point
        if self.detected_player:
            dx = global_vars.player.x - self.x
            dy = global_vars.player.y - self.y
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
                
            if global_vars.player.attack_on:
                self.get_attacked(distance)
            
        new_x = self.x + dx * self.speed * global_vars.dt
        new_y = self.y + dy * self.speed * global_vars.dt
        
        
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
            
        self.speed += (self.acceleration + 1 * 10) * global_vars.dt
        self.speed *= pow(0.5, global_vars.dt * 60)

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
            self.transmission_cooldown -= global_vars.dt
            if self.transmission_cooldown < 0:
                self.transmission_cooldown = 0
        
        if self.detected_player and self.transmission_cooldown == 0:
            if random.random()*10 < 0.3:
                theta = math.radians(global_vars.player.angle)
                x = global_vars.player.x - math.sin(theta) * 80
                y = global_vars.player.y + math.cos(theta) * 80
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
