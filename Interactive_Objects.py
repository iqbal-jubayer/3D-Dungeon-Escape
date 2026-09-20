from Utilities import *


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
        
        distance = getDistance(self.x, self.y, global_vars.player.x, global_vars.player.y)
        if distance < self.width:
            if self.locked:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "[LOCKED]")
            elif self.closed:
                draw_text(0, -WINDOW_SIZE[1]//2 + 50, "Press \'f\'")
    
    def update(self):
        if self.closed:
            if self.opening_angle > 0:
                self.opening_angle -= 100 * global_vars.dt
        else:
            if self.opening_angle < 90:
                self.opening_angle += 100 * global_vars.dt
        
    def keyboard_listener(self, key):
        if key == b'f' and self.closed:
            distance = getDistance(self.x, self.y, global_vars.player.x, global_vars.player.y)
            if distance < self.width:
                if not self.locked:
                    self.closed = not self.closed
                else:
                    if global_vars.CHEAT_MODE:
                        self.locked = False
                        self.closed = not self.closed
                    else:
                        for name, color in global_vars.player.keys:
                            if name == self.required_key_name:
                                self.locked = False
                                self.closed = not self.closed
                                global_vars.player.keys.remove((self.required_key_name, color))
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
        super().update()
        if not self.closed:
            self.over = True
        if self.over:
            if self.t < 100:
                self.t += 1
            else:
                global_vars.GAME_STATE = GAME_STATES['ESCAPED']
                self.over = False