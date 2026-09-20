from Utilities import *

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
        distance = math.sqrt((self.x - global_vars.player.x)**2 + (self.y - global_vars.player.y)**2)
        if distance < self.width//2 + global_vars.player.width//2 and global_vars.player.z - global_vars.player.height//2 < 10:
            global_vars.player.get_damage(self.damage)
            
            theta = math.radians(global_vars.player.angle)
            fx = math.sin(theta)
            fy = -math.cos(theta)
            
            dx = global_vars.player.x - self.x
            dy = global_vars.player.y - self.y
            distance = getDistance(self.x, self.y, global_vars.player.x, global_vars.player.y)
            dx = dx/distance
            dy = dy/distance
            
            dot = -(dx * fx + dy * fy)
            if dot < 0:
                global_vars.player.speed += 50
            else:
                global_vars.player.speed -= 50
