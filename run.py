# Name: Jubayer Iqbal
# ID: 24101512

import os

os.environ["PYOPENGL_PLATFORM"] = "glx"

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = (0,-500,400)

fovY = 120  # Field of view

WINDOW_SIZE = (1000,800)
WINDOW_TITLE = b"Game"
FPS = 60

# GAME_STATE
#   - MENU
#   - HELP
#   - GAME
GAME_STATE = "GAME"

# classes
class CAMERA:
    camera_x = 0
    camera_y = 0
    camera_z = 0

    target_x = 0
    target_y = 0
    target_z = 0

    def __init__(self):
        self.distance = 80

    def update(self):
        self.camera_x = 0
        self.camera_y = 1
        self.camera_z = 500
        
        self.target_x = 0
        self.target_y = 0
        self.target_z = 0
        return
        theta = math.radians(player.angle)
        fx = math.sin(theta)
        fy = -math.cos(theta)
        
        self.camera_x = player.x - fx * self.distance
        self.camera_y = player.y - fy * self.distance
        self.camera_z = 120
        
        self.target_x = player.x
        self.target_y = player.y
        self.target_z = 90

class STARTROOM:
    x = 0
    y = 0
    width = 1000
    length = 500
    tile_size = 50
    
    angle = 0
    wall = []
    
    def __init__(self):
        self.countX = (self.width // self.tile_size)//2
        self.countY = (self.length // self.tile_size)//2
        
        self.wall.append(
            WALL_V(self.width//2 + self.tile_size, self.length//2 - self.tile_size//2, self.tile_size, self.length)
        )
        self.wall.append(
            WALL_V(-self.width//2, self.length//2 - self.tile_size//2, self.tile_size, self.length)
        )
        
        self.wall.append(
            WALL_H(self.width//2, self.length//2 - self.tile_size//2, self.tile_size, self.width - self.tile_size)
        )
        
        self.wall.append(
            WALL_H(self.width//2, -self.length//2 - self.tile_size//2, self.tile_size, self.width//2 - self.tile_size*2)
        )
        
        self.wall.append(
            WALL_H(-self.tile_size, -self.length//2 - self.tile_size//2, self.tile_size, self.width//2 - self.tile_size*2)
        )
    
    def draw(self):
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angle, 0, 0, 1)
        
        glPushMatrix()
        
        glPushMatrix()
        for i in range(-self.countX, self.countX+1, 1):
            for j in range(-self.countY, self.countY+1, 1):
                draw_rect(i*self.tile_size, j*self.tile_size, self.tile_size, self.tile_size, color=(206/255, 109/255, 58/255))
        glPopMatrix()
        
        for wall in self.wall:
            wall.draw()
        
        glPopMatrix()

    def collision(self):
        for wall in self.wall:
            collided = wall.collision()
            if collided:
                return True
        return False
    
class WALL_V:
    height = 200
    
    def __init__(self, x, y, depth, width):
        self.x = x
        self.y = y
        self.z = depth//2
        self.depth = depth
        self.width = width
    
    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(self.x, self.y, self.z)
        for j in range(self.height//self.depth):
            glPushMatrix()
            for i in range(self.width//self.depth + 1):
                glutSolidCube(self.depth)
                glTranslatef(0, -self.depth, 0)
            glPopMatrix()
            glTranslatef(0, 0, self.depth)
        glPopMatrix()
    
    def collision(self):
        min_x = self.x - self.depth / 2
        max_x = self.x + self.depth / 2

        max_y = self.y
        min_y = self.y - self.width

        if (
            player.x + 20 > min_x and
            player.x - 20 < max_x and
            player.y + 20 > min_y and
            player.y - 20 < max_y
        ):
            return True

        return False
        
class WALL_H:
    height = 200
    
    def __init__(self, x, y, depth, width):
        self.x = x
        self.y = y
        self.z = depth//2
        self.depth = depth
        self.width = width
    
    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(self.x, self.y, self.z)
        for j in range(self.height//self.depth):
            glPushMatrix()
            for i in range(self.width//self.depth + 1):
                glutSolidCube(self.depth)
                glTranslatef(-self.depth, 0, 0)
            glPopMatrix()
            glTranslatef(0, 0, self.depth)
        glPopMatrix()
        
    def collision(self):
        pass

class Player:
    x = 0
    y = 0
    
    speed = 0
    acc = 3
    rot_acc = 5
    
    angle = 0
    
    def __init__(self):
        pass
    
    def draw(self):
        glColor3f(1, 0, 0)
        glPushMatrix()
        glTranslatef(self.x, self.y, 20)
        glRotatef(self.angle, 0, 0, 1)
        glutSolidCube(40)
        glTranslatef(0, 0, 20)
        glutSolidCube(40)
        glPopMatrix()
        
    def update(self):
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed
        self.speed *= 0.5

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
        draw_text(self.x + self.width//2 - 30, self.y-self.height//2, self.text, color=(0,0,0))
        
    def click(self, mouseX, mouseY, callback=None):
        if self.y - self.height < mouseY < self.y and self.x < mouseX < self.x + self.width:
            if callback is not None:
                callback()


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
    glOrtho(-WINDOW_SIZE[0]//2, WINDOW_SIZE[0]//2, -WINDOW_SIZE[1]//2, WINDOW_SIZE[1]//2, 0, 1)

    
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
    glVertex3f(x, y, 0)
    
    glColor3f(r1, g1, b1)
    glVertex3f(x+width, y, 0)
    
    glColor3f(r2, g2, b2)
    glVertex3f(x+width, y-height, 0)
    
    glColor3f(r3, g3, b3)
    glVertex3f(x, y-height, 0)
    glEnd()

# Callbacks
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    
    if key == b'w':
        # start_room.y -= 5
        player.speed += 3
    if key == b's':
        # start_room.y += 5
        player.speed -= 3
    if key == b'a':
        # start_room.x += 5
        player.angle += 5
    if key == b'd':
        # start_room.x -= 5
        player.angle -= 5
        
    if key == b'\x1b':
        glutLeaveMainLoop()

def specialKeyListener(key, x, y):
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        camera.camera_z -= 5
        
    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        camera.camera_z += 5
        
    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        start_room.angle += 1

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        start_room.angle -= 1

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
        # Left mouse button fires a bullet
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            pass

        # Right mouse button toggles camera tracking mode
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            pass

def idle(value=0):
    player.update()
    camera.update()
    start_room.collision()
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
start_button = BUTTON(-250, 100, 500, 50, text="START")
def start_button_callback():
    global GAME_STATE
    GAME_STATE = "GAME"

help_button =  BUTTON(-250, 40, 500, 50, text="HELP")
def help_button_callback():
    global GAME_STATE
    GAME_STATE = "HELP"
help_back_button =  BUTTON(-480, 325, 100, 50, text="<-Back")
def help_back_button_callback():
    global GAME_STATE
    GAME_STATE = "MENU"
    
exit_button =  BUTTON(-250, -20, 500, 50, text="EXIT")

# Creating Objects
start_room = STARTROOM()
camera = CAMERA()
player = Player()
    
def draw_menu():
    glColor3f(1, 0, 0)
    draw_rect(-WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(-12*5, 200, "3D Dungeon", font=GLUT_BITMAP_TIMES_ROMAN_24)
    
    start_button.draw()
    help_button.draw()
    exit_button.draw()

def draw_help():
    glColor3f(1, 0, 0)
    draw_rect(-WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2, WINDOW_SIZE[0], WINDOW_SIZE[1], color=(0,0,0.8), color1=(0,0,0.8), color2=(0,0,0), color3=(0,0,0))
    
    draw_text(-12*5, 300, "HELP", font=GLUT_BITMAP_TIMES_ROMAN_24)
    help_back_button.draw()

def draw_brick(x, y, z, width, height,color=(1,0,0)):
    a = width//2
    
    glPushMatrix()
    r, g, b = color
    glColor3f(r, g, b)
    
    glTranslatef(x, y, z)
    glutSolidCube(a)
    glTranslatef(0, a, 0)
    glutSolidCube(a)
    
    glColor3f(0.4, 0.4, 0.4)
    glTranslatef(0, 0, a)
    glutSolidCube(a-1)
    glTranslatef(0, -a, 0)
    glutSolidCube(a-1)
    glTranslatef(0, -a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, 0, -a//2)
    glutSolidCube(a-1)
    glTranslatef(0, a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, a, 0)
    glutSolidCube(a-1)
    glTranslatef(0, a//2, 0)
    glutSolidCube(a-1)
    glTranslatef(0, 0, a)
    glutSolidCube(a-1)
    glTranslatef(0, 0, a//2)
    glutSolidCube(a-1)
    
    glPopMatrix()

def draw_game():
    start_room.draw()
    player.draw()
    
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
        setupCamera()  # Configure camera perspective
        draw_game()
        
    
    glutSwapBuffers()

# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(WINDOW_SIZE[0], WINDOW_SIZE[1])  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(WINDOW_TITLE)  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutTimerFunc(1000//FPS, idle, 0)

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
