from Utilities import *

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

    def update(self, player):
        theta = math.radians(player.angle)
        fx = math.sin(theta)
        fy = -math.cos(theta)
        
        if self.target_up >= 45:
            self.target_up = 45
        elif self.target_up <= -25:
            self.target_up = -25
        
        if global_vars.VIEW_MODE == 0:
            self.camera_x = player.x + fx * 20
            self.camera_y = player.y - fy * -20
            self.camera_z = player.z + player.height//2
            
            self.target_x = player.x + fx * self.distance * 2
            self.target_y = player.y + fy * self.distance * 2
            self.target_z = player.z + player.height//2
            
        elif global_vars.VIEW_MODE == 1:
            self.camera_x = player.x - fx * self.distance
            self.camera_y = player.y - fy * self.distance
            self.camera_z = player.z + player.height + self.target_up
            
            self.target_x = player.x + fx * self.distance
            self.target_y = player.y + fy * self.distance
            self.target_z = player.z + player.height//2
            
        elif global_vars.VIEW_MODE == 2:
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

def setupCamera(camera):
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
