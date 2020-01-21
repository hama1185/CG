from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import numpy as np
import time
import threading

class controlArm():
    def __init__(self, l, j, k):
        self.l = l
        self.j = j
        self.k = k

    #mathmatica`s atan is (x,y),but python`s atan is (y,x)

    def solveArm(self, x, y, z):
        global spaceFlag, dx, dy, dz
        if spaceFlag:
            spaceFlag = False
            minsub = 100.0
            dataFirstArm = 0.0
            dataSecondArm = 0.0
            dataThirdArm = 0.0
            for n in range(-180, 180, 5):
                a = n
                for i in range(-80, 80):
                    b = i
                    for j in range(-80, 80):
                        c = j
                        radA = math.radians(a)
                        radB = math.radians(b)
                        radC = math.radians(c)
                        solveX = -self.j * math.cos(radA) * math.sin(radB) - self.k * math.cos(radC) * math.sin(radB) * math.cos(radA) + self.k * math.sin(radA) * math.sin(radC)
                        solveY = self.l + self.j * math.cos(radB) + self.k * math.cos(radB) * math.cos(radC)
                        solveZ = self.j * math.sin(radA) * math.sin(radB) + self.k * math.cos(radC) * math.sin(radB) * math.sin(radA) + self.k * math.cos(radA) * math.sin(radC)

                        substractX = abs(x - solveX)
                        substractY = abs(y - solveY)
                        substractZ = abs(z - solveZ)

                        sumSub = substractX + substractY + substractZ
                        if sumSub < minsub:
                            minsub = sumSub
                            dataFirstArm = a
                            dataSecondArm = b
                            dataThirdArm = c

            ansList = np.array([dataFirstArm,dataSecondArm,dataThirdArm],dtype=int)
            print(substractX)
            print(substractY)
            print(substractZ)
            print(dataFirstArm)
            print(dataSecondArm)
            print(dataThirdArm)
            return ansList
        
        else:
            angleList = np.array([dy, dz, dx],dtype=int)
            return angleList
    

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
# g is global
 
gx = 0.0
gy = 0.0
gz = 0.0

# p is position

px = 0.0
py = 0.0
pz = 0.0

# d is delta

dx = 0.0
dy = 0.0
dz = 0.0

# m is mind

mx = 0.0
my = 0.0
mz = 0.0
spaceFlag = False
isFinish = False

GROUND_LEVEL = -2.0
BASE_HALF_THICKNESS = 0.2
ARM_SIZE = 0.3
ARM_HALF_LENGTH = 1.2


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


def animation(fromList,toList):
    global mx,my,mz,isFinish
    refresh()
    total = 0
    print("animation start")
    if fromList[0] > toList[0]:
        for i in range(toList[0] , fromList[0] + 1):
            my = my - 1
            time.sleep(0.01)

    elif fromList[0] < toList[0]:
        for i in range(fromList[0], toList[0] + 1):
            my = my + 1
            time.sleep(0.01)

    if fromList[1] > toList[1]:
        for j in range(toList[1] , fromList[1] + 1):
            mz = mz - 1
            time.sleep(0.01)

    elif fromList[1] < toList[1]:
        for j in range(fromList[1], toList[1] + 1):
            mz = mz + 1
            time.sleep(0.01)
    
    if fromList[2] > toList[2]:
        for k in range(toList[2] , fromList[2] + 1):
            mx = mx - 1
            time.sleep(0.01)

    elif fromList[2] < toList[2]:
        for k in range(fromList[2], toList[2] + 1):
            mx = mx + 1
            time.sleep(0.01)

    print("animation finish")
    isFinish = True


def refresh():
    glutPostRedisplay()


def loopRefresh():
    global isFinish
    while not isFinish:
        time.sleep(0.05)
        refresh()


def rundisplay():
    global gx,gy,gz,dx,dy,dz,spaceFlag
    if spaceFlag:
        ControlArm = controlArm(ARM_HALF_LENGTH,ARM_HALF_LENGTH,ARM_HALF_LENGTH)
        toList = ControlArm.solveArm(gx, gy, gz)
        fromList = np.array([my, mz, mx],dtype=int)
        threadFront = threading.Thread(target=loopRefresh)
        threadBack = threading.Thread(target=animation,args=(fromList, toList,))
        
        threadFront.start()
        threadBack.start()


def display():
    global mx,my,mz
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, LIGHTPOS)

    glTranslated(0.0, 0.0, -10.0)

    myGround(GROUND_LEVEL)
    glRotated(my, 0.0, 1.0, 0.0)

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
    glRotated(mz, 0.0, 0.0, 1.0)
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    myBox(VERTEX_ARM)

# 2nd joint
    glTranslated(0.0, ARM_HALF_LENGTH, 0.0)
    glPushMatrix()
    glRotated(90.0, 0.0, 0.0, 1.0)
    myCylinder(0.4, 0.4, 16)
    glPopMatrix()

# 3nd arm
    glRotated(mx, 1.0, 0.0, 0.0)
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
    global pz,py
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            py = x
            pz = y


def motion(x, y):
    global dz,dy,pz,py,mz,my
    dy = x - py
    dz = y - pz
    if dz > 80:
        dz = 80
    if dz < -80:
        dz = -80
    mz = dz
    my = dy
    refresh()


def mouseWheel(button, dir, x, y):
    global dx,mx
    if dir > 0:
        dx += 2
    elif dir < 0:
        dx -= 2

    if dx > 80:
        dx = 80
    if dx < -80:
        dx = -80
    
    mx = dx
    refresh()


def key(key, x, y):
    global gx,gy,gz
    key = key.decode("utf-8")
    if key == " ":
        inputData()
        rundisplay()


def inputData():
    global gx,gy,gz,spaceFlag
    spaceFlag = True 
    gx = input("x :\n")
    while type(gx) != (float or int):
        try:
            gx = float(gx)
        except ValueError:
            gx = input("x :\n")
    gy = input("y :\n")
    while type(gy) != (float or int):
        try:
            gy = float(gy)
        except ValueError:
            gy = input("y :\n")
    gz = input("z :\n")
    while type(gz) != (float or int):
        try:
            gz = float(gz)
        except ValueError:
            gz = input("z :\n")


inputData()
VERTEX_ARM = vertex_box(ARM_SIZE, ARM_HALF_LENGTH, ARM_SIZE)
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
glutCreateWindow(b"GLUT robot arm")
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutMouseWheelFunc(mouseWheel)
glutKeyboardUpFunc(key)
glutReshapeFunc(resize)
glutIdleFunc(refresh)
init()
glutMainLoop()