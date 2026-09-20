from Utilities import *

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
        distance = getDistance(self.x + self.col_x, self.y + self.col_y, global_vars.player.x, global_vars.player.y)
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
        self.lightness += global_vars.dt * self.l_dir
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
                
                distance = getDistance(rect_x + self.x, rect_y + self.y, global_vars.player.x, global_vars.player.y)
                if distance > global_vars.DRAWING_RADIUS:
                    continue
                
                r, g, b, a = self.floor_light_up(rect_x, rect_y, global_vars.player.x, global_vars.player.y, (r, g, b, a), self.lightness, self.max_lightness)
                    
                for item in global_vars.static_item_list:
                    if not item.isLightSource:
                        continue
                    r, g, b, a = self.floor_light_up(rect_x, rect_y, item.x, item.y, (r, g, b, a), item.lightness, item.max_lightness)
                        
                for item in global_vars.item_list:
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
            distance = getDistance(obj.x + self.x, obj.y + self.y, global_vars.player.x, global_vars.player.y)
            if distance < global_vars.DRAWING_RADIUS:
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
            
        self.lightness += global_vars.dt * self.l_dir
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
    def __init__(self, x, y, width, length, tile_size=50, type="", wall_color=(0.1, 0.1, 0.2, 1), floor_color=(0, 0, 0, 1)):
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
