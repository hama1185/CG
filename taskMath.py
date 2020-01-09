import sys
import math

class controlArm():
    def __init__(self, l, j):
        self.l = l
        self.j = j

    def controlFirstArm(x ,y ,z):
        print(math.degrees(math.atan2(z,-x)))

    def controlSecondArm(self, x ,y ,z):
        #mathmatica`s atan is (x,y),but python`s atan is (y,x)
        try:
            print(math.degrees(math.acos( (y - self.l) / self.j )))
        except ValueError:
            print("Not Reach")

classMethod = controlArm(50,50)

for i in range(-25,25):
    for j in range(-25,25):
        for k in range(-25,25):
            classMethod.controlSecondArm(i,j,k)