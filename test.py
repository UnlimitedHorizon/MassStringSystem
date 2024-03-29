import sys, random, time
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import numpy as np

outfile = open("outfile.output", "w")

maxLevel = 2
class Element:
    def __init__(self):
        self.mass = 1
        self.damping = -0.1

        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        

windowWidth = 640
windowHeight = 480
class System:
    def __init__(self, n):
        self.elements = []
        self.n = n
        self.axis = np.array([0, 1, 0])
        # self.axisK = -0.1
        self.axisK = 0.0
        self.kList = np.array([[1, 2, 0, 2, 1] for x in range (self.n)])
        self.restLengthList = np.zeros((self.n, 2*maxLevel+1))
        self.accumulateTime = 0.0

        self.generate()

    def generate(self):
        for i in range(self.n):
            e = Element()
            e.position = np.array([windowWidth/2, i*100, 0], dtype = float)
            self.elements.append(e)


        # initialize rest length of springs
        for level in range(1, maxLevel + 1):
            for i in range(self.n - level):
                e = self.elements[i]
                eNext = self.elements[i + level]
                vec = eNext.position - e.position
                self.restLengthList[i][maxLevel + level] = self.restLengthList[i + level][maxLevel - level] = np.linalg.norm(vec)


    def animate(self, deltaT):
        self.accumulateTime += deltaT
        externalAcc = np.array([5, 9.8, 0])
        tempVelocities = np.zeros((self.n, 3))
        tempPositions = np.zeros((self.n, 3))
        outfile.write("dT={:.3f}: ".format(deltaT))
        position0 = self.elements[0].position
        for i in range(1, self.n):
            e = self.elements[i]
            resultantForce = np.zeros(3)
            for j in range(max(0, i-maxLevel), min(self.n, i+maxLevel+1)):
                if j != i:
                    e2 = self.elements[j]
                    vec = e.position - e2.position
                    level = j - i
                    k = self.kList[i][maxLevel + level]
                    restLength = self.restLengthList[i][maxLevel + level]
                    vec = e2.position - e.position
                    length = np.linalg.norm(vec)
                    f = k * (1 - restLength/length) * vec
                    resultantForce += f
            # 质点间的弹簧弹力给予的加速度
            resultantAcc = resultantForce/e.mass
            # 外力加速度（重力加速度/……）
            resultantAcc += externalAcc
            # 速度阻尼加速度
            resultantAcc += e.velocity*e.damping
            # 向心力
            vec = e.position - position0
            resultantAcc += self.axisK * (vec - self.axis * np.dot(self.axis, vec) / np.linalg.norm(self.axis))

            tempPositions[i] = e.position + (e.velocity + resultantAcc * deltaT / 2) * deltaT
            tempVelocities[i] = e.velocity + resultantAcc * deltaT
            outfile.write("point{}:a={:7.3f}, p={:7.3f}, v={:7.3f}; ".format(i, resultantAcc[1], tempPositions[i][1], tempVelocities[i][1]))
        outfile.write("\n")

        for i in range(1, self.n):
            self.elements[i].position = tempPositions[i]
            self.elements[i].velocity = tempVelocities[i]

            


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.s = System(5)
        self.lastTime = time.time()
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process)
        self.timer.start(1/15)

    def initUI(self):
        self.setGeometry(300, 300, windowWidth, windowHeight)
        self.setWindowTitle("Test")
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawSystem(qp)
        qp.end()

    def process(self):
        currentTime = time.time()
        self.s.animate(currentTime - self.lastTime)
        self.lastTime = currentTime
        self.update()

    def drawSystem(self, qp):
        elements = self.s.elements
        eLast = None
        for e in elements:
            qp.setPen(QPen(Qt.blue, 4, Qt.SolidLine));
            radius = 30
            qp.drawEllipse(e.position[0]-radius/2, windowHeight - e.position[1]-radius/2, radius, radius);
            if eLast is not None:
                qp.drawLine(
                    e.position[0], windowHeight - e.position[1],
                    eLast.position[0], windowHeight - eLast.position[1])
            eLast = e

    def drawPoints(self, qp):
        qp.setPen(Qt.red)
        size = self.size()

        for i in range(1000): 
            x = random.randint(1, size.width()-1)
            y = random.randint(1, size.height()-1)
            qp.drawPoint(x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# def listAppend(l, e):
#     l.append(e)
# l = list()


# def test(x, y):
#     print('x:' + str(id(x)) + ', y:' + str(id(y)))
#     x.append(1)
#     print('x:' + str(id(x)))
#     x+=y
#     print('x:' + str(id(x)))
#     print(x)
# a=list()
# print('a:' + str(id(a)))
# a.append(1)
# print('a:' + str(id(a)))
# b=[2,3]
# print('b:' + str(id(b)))
# test(a,b)
# print(a)

# listAppend(l, 1)
# print(l)
# listAppend(l, "test")
# print(l)
# listAppend(l, True)
# print(l)



