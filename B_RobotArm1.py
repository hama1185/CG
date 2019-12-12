from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

class Face:
    def __init__(self, i_vertex, normal):
        self.i_vertex = i_vertex
        self.normal = normal

FACE = [
    Face([3, 2, 1, 0], [ 0.0,  0.0, -1.0]),
    Face([2, 6, 5, 1], [ 1.0,  0.0,  0.0]),
    Face([6, 7, 4, 5], [ 0.0,  0.0,  1.0]),
    Face([7, 3, 0, 4], [-1.0,  0.0,  0.0]),
    Face([0, 1, 5, 4], [ 0.0, -1.0,  0.0]),
    Face([7, 6, 2, 3], [ 0.0,  1.0,  0.0])]

LIGHTPOS = [3.0, 4.0, 5.0, 1.0]
RED = [0.8, 0.2, 0.2, 1.0]
BLUE = [0.2, 0.2, 0.8, 1.0]
YELLOW = [0.8, 0.8, 0.2, 1.0]
DIFFUSE_GROUND = [[0.6, 0.6, 0.6, 1.0], [0.3, 0.3, 0.3, 1.0]]
RANGE_GROUND = range(-5, 5)

dx = 0
dy = 0
dz = 0
gx = 0
gy = 0
gz = 0

GROUND_LEVEL = -2.0
BASE_HALF_THICKNESS = 0.2
ARM_SIZE = 0.3
ARM_HALF_LENGTH = 1.0

def vertex_box(x, y, z):
    vertex = [
        [-x, -y, -z],   # A
        [ x, -y, -z],   # B
        [ x,  y, -z],   # C
        [-x,  y, -z],   # D
        [-x, -y,  z],   # E
        [ x, -y,  z],   # F
        [ x,  y,  z],   # G
        [-x,  y,  z]]   # H
    return vertex
    
def myBox(vertex):
    glMaterialfv(GL_FRONT, GL_DIFFUSE, RED)
    
    glBegin(GL_QUADS)
    for face1 in FACE:
        glNormal3dv(face1.normal)
        for i in face1.i_vertex:
            glVertex3dv(vertex[i])
    glEnd()    

def myCylinder(radius, height, sides):
    step = 2*math.pi/sides
    glMaterialfv(GL_FRONT, GL_DIFFUSE, YELLOW)

# top
    glNormal3d(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3d(0.0, height, 0.0)
    for i in range(sides+1):
        t = i*step
        glVertex3d(radius*math.sin(t), height, radius*math.cos(t))
    glEnd()    

# bottom
    glNormal3d(0.0, -1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    for i in reversed(range(sides+1)):
        t = i*step
        glVertex3d(radius*math.sin(t), -height, radius*math.cos(t))
    glEnd()    

# side
    glBegin(GL_QUAD_STRIP)
    for i in range(sides+1):
        t = i*step
        s = math.sin(t)
        c = math.cos(t)
        x = radius*s
        z = radius*c
        glNormal3d(s, 0.0, c)
        glVertex3d(x, height, z)
        glVertex3d(x, -height, z)
    glEnd()

def controlFirstArm(x ,y ,z):
    global gy
    return gy

def controlSecondArm(x ,y ,z):
    global gz
    return gz

def controlThirdArm(x ,y ,z):
    global gx
    return gx

def myGround(height):
    glBegin(GL_QUADS)
    glNormal3d(0.0, 1.0, 0.0)
    for j in RANGE_GROUND:
        for i in RANGE_GROUND:
            glMaterialfv(GL_FRONT, GL_DIFFUSE, \
                DIFFUSE_GROUND[(i+j)&1])
            glVertex3d(i, height, j)
            glVertex3d(i, height, j+1)
            glVertex3d(i+1, height, j+1)
            glVertex3d(i+1, height, j)
    glEnd()

def display():
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, LIGHTPOS)

    glTranslated(0.0, 0.0, -10.0)

    myGround(GROUND_LEVEL)
    glRotated(gx, 0.0, 1.0, 0.0)

# base
    glTranslated(0.0, GROUND_LEVEL+BASE_HALF_THICKNESS, 0.0)
    myCylinder(1.0, BASE_HALF_THICKNESS, 16)

# 1st arm
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    myBox(VERTEX_ARM)

# 1st joint
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    glPushMatrix()
    glRotated(90.0, 1.0, 0.0, 0.0)
    myCylinder(0.4, 0.4, 16)
    glPopMatrix()

# 2nd arm
    glRotated(gy, 0.0, 0.0, 1.0)
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    myBox(VERTEX_ARM)

# 2nd joint
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    glPushMatrix()
    glRotated(90.0, 0.0, 0.0, 1.0)
    myCylinder(0.4, 0.4, 16)
    glPopMatrix()

# 3nd arm
    glRotated(gy, 1.0, 0.0, 0.0)
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    myBox(VERTEX_ARM)

# hand
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, BLUE)
    glutSolidCube(0.9)

    glFlush()

def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(34.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def init():
    gray = 1.0
    glClearColor(gray, gray, gray, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def mouse(button, state, x, y):
    global dx,dy
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            dx = x
            dy = y

def motion(x, y):
    global gx,gy
    gx = x - dx
    gy = y - dy
    
    glutPostRedisplay()


VERTEX_ARM = vertex_box(ARM_SIZE, ARM_HALF_LENGTH, ARM_SIZE)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
glutCreateWindow(b"GLUT robot arm")
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutReshapeFunc(resize)
init()
glutMainLoop()