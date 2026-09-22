from Utilities import *
from Menu import *
from Camera import *
from Level import *
from World import *

global_vars.level = Level()
camera = CAMERA()
global_vars.world = World() 
global_vars.world.load_level("1")
menu = Menu()

# Callbacks
def keyboardDownListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    if global_vars.GAME_STATE == GAME_STATES["GAME"]:
        global_vars.level.keyboardDownListener(key, x, y)
            
    elif global_vars.GAME_STATE == GAME_STATES["SELECT WORLD"]:
        if key == b'\x1b':
            global_vars.GAME_STATE = GAME_STATES["MAINMENU"]
            
    elif global_vars.GAME_STATE == GAME_STATES["MAINMENU"]:
        if key == b'\x1b':
            glutLeaveMainLoop()

def keyboardUpListener(key, x, y):
    pass

def specialKeyListener(key, x, y):
    # Move camera up (UP arrow key)
    if global_vars.GAME_STATE == GAME_STATES["GAME"]:
        if global_vars.PAUSE:
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
            global_vars.player.sprint = not global_vars.player.sprint

def mouseListener(button, state, x, y):
    x, y = convert_coordinate(x, y, WINDOW_SIZE[0], WINDOW_SIZE[1])
    
    if global_vars.GAME_STATE == GAME_STATES["GAME"]:
        global_vars.hud.mouseListener(button, state, x, y)
        
        if global_vars.PAUSE:
            return
        global_vars.player.mouseListener(button, state, x, y)
        
        if button == 3:
            camera.target_up += 1
        if button == 4:
            camera.target_up -= 1
    else:
        menu.mouseListener(button, state, x, y)
        

last_time = time.time()
def idle(value=0):
    global last_time
    
    current_time = time.time()
    global_vars.dt = current_time - last_time
    last_time = current_time
    global_vars.dt = min(global_vars.dt, 1/FPS)
    
    if global_vars.GAME_STATE == GAME_STATES["SELECT WORLD"]:
        if global_vars.SELECTED_WORLD != -1:
            global_vars.GAME_STATE = GAME_STATES["GAME"]
            global_vars.world.load_level(global_vars.SELECTED_WORLD)
            
    elif global_vars.GAME_STATE == GAME_STATES['GAME']:
        if global_vars.PAUSE:
            glutPostRedisplay()
            glutTimerFunc(int(1000/FPS), idle, 0)
            return
        global_vars.SECONDS += global_vars.dt
        global_vars.player.update()
        camera.update(global_vars.player)
        global_vars.hud.update()
        global_vars.level.update()
        
    else:
        global_vars.SELECTED_WORLD = -1
    
    glutPostRedisplay()
    glutTimerFunc(int(1000/FPS), idle, 0)
    
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
    
    if global_vars.GAME_STATE == GAME_STATES["GAME"]:
        glEnable(GL_DEPTH_TEST)
        setupCamera(camera)
        global_vars.level.draw()
        global_vars.player.draw()
        global_vars.hud.draw()
        camera.draw()
    else:
        menu.draw()

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
    glutKeyboardFunc(keyboardDownListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutTimerFunc(int(1000/FPS), idle, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
