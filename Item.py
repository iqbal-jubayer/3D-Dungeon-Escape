from Utilities import *

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
            if collided_with == global_vars.player:
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
        global_vars.player.keys.append((self.name, self.color))

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
        if global_vars.player.health < global_vars.player.max_health:
            global_vars.player.health += 15
        if global_vars.player.health > global_vars.player.max_health:
            global_vars.player.health = global_vars.player.max_health
        
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
        if global_vars.player.shield < global_vars.player.max_shield:
            global_vars.player.shield += 30
        if global_vars.player.shield > global_vars.player.max_shield:
            global_vars.player.shield = global_vars.player.max_shield
