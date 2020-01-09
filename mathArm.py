import sys
import math

class controlArm():
    def __init__(self, l, j, k):
        self.l = l
        self.j = j
        self.k = k
        self.l2 = l ** 2
        self.j2 = j ** 2
        self.k2 = k ** 2
        self.l3 = l ** 3
        self.j3 = j ** 3
        self.k3 = k ** 3
        self.l4 = l ** 4
        self.j4 = j ** 4
        self.k4 = k ** 4

    def controlFirstArm(x ,y ,z):
        print("a")

    def controlSecondArm(self, x ,y ,z):
        #mathmatica`s atan is (x,y),but python`s atan is (y,x)
        x2 = x ** 2
        y2 = y ** 2
        z2 = z ** 2
        x3 = x ** 3 
        y3 = y ** 3
        z3 = z ** 3
        x4 = x ** 4
        y4 = y ** 4
        z4 = z ** 4
        argumentX = -((2 * (self.j * self.l-self.j * y))/(self.j2-self.k2+self.l2+x2-2 * self.l * y+y2+z2))
        argumentY = -(((self.j4-2 * self.j2 * self.k2+self.k4-2 * self.j2 * self.l2-2 * self.k2 * self.l2+self.l4+2 * self.j2 * x2-2 * self.k2 * x2+2 * self.l2 * x2+x4+4 * self.j2 * self.l * y+4 * self.k2 * self.l * y-4 * self.l3 * y-4 * self.l * x2 * y-2 * self.j2 * y2-2 * self.k2 * y2+6 * self.l2 * y2+2 * x2 * y2-4 * self.l * y3+y4+2 * self.j2 * z2-2 * self.k2 * z2+2 * self.l2 * z2+2 * x2 * z2-4 * self.l * y * z2+2 * y2 * z2+z4) ** 0.5)/((self.j4-2 * self.j2 * self.k2+self.k4+2 * self.j2 * self.l2-2 * self.k2 * self.l2+self.l4+2 * self.j2 * x2-2 * self.k2 * x2+2 * self.l2 * x2+x4-4 * self.j2 * self.l * y+4 * self.k2 * self.l * y-4 * self.l3 * y-4 * self.l * x2 * y+2 * self.j2 * y2-2 * self.k2 * y2+6 * self.l2 * y2+2 * x2 * y2-4 * self.l * y3+y4+2 * self.j2 * z2-2 * self.k2 * z2+2 * self.l2 * z2+2 * x2 * z2-4 * self.l * y * z2+2 * y2 * z2+z4) ** 0.5))
        # b = math.atan2(argumentY,argumentX)
        c = ((self.j4-2 * self.j2 * self.k2+self.k4+2 * self.j2 * self.l2-2 * self.k2 * self.l2+self.l4+2 * self.j2 * x2-2 * self.k2 * x2+2 * self.l2 * x2+x4-4 * self.j2 * self.l * y+4 * self.k2 * self.l * y-4 * self.l3 * y-4 * self.l * x2 * y+2 * self.j2 * y2-2 * self.k2 * y2+6 * self.l2 * y2+2 * x2 * y2-4 * self.l * y3+y4+2 * self.j2 * z2-2 * self.k2 * z2+2 * self.l2 * z2+2 * x2 * z2-4 * self.l * y * z2+2 * y2 * z2+z4) ** 0.5)
        a = abs(((self.j4-2 * self.j2 * self.k2+self.k4-2 * self.j2 * self.l2-2 * self.k2 * self.l2+self.l4+2 * self.j2 * x2-2 * self.k2 * x2+2 * self.l2 * x2+x4+4 * self.j2 * self.l * y+4 * self.k2 * self.l * y-4 * self.l3 * y-4 * self.l * x2 * y-2 * self.j2 * y2-2 * self.k2 * y2+6 * self.l2 * y2+2 * x2 * y2-4 * self.l * y3+y4+2 * self.j2 * z2-2 * self.k2 * z2+2 * self.l2 * z2+2 * x2 * z2-4 * self.l * y * z2+2 * y2 * z2+z4) ** 0.5))
        # print(math.degrees(b))
        argumentX = -((2 * (self.j * self.l-self.j * y))/(self.j2-self.k2+self.l2+x2-2 * self.l * y+y2+z2))
        argumentY = -(c/a)
        
        b = math.atan2(argumentY,argumentX)
        print(math.degrees(b))

    def controlThirdArm(x ,y ,z):
        print("c")

classMethod = controlArm(100,100,100)

for i in range(-25,25):
    for j in range(-25,25):
        for k in range(-25,25):
            classMethod.controlSecondArm(i,j,k)
