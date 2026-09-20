from Utilities import *

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
        self.lightness += global_vars.dt*self.l_dir
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
