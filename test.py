import sys, random, time
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer
import numpy as np

outfile = open("outfile.txt", "w")

maxLevel = 2
class Element:
    def __init__(self):
        self.mass = 1
        self.damping = 0.5

        self.position = np.zeros(3)
        # self.lastPostion = np.zeros(3)

        self.velocity = np.zeros(3)

        # self.preKList = [0 for x in range(maxLevel)]
        # self.nextKList = [0 for x in range(maxLevel)]
        # self.preRestLengthList = [0 for x in range(maxLevel)]
        # self.nextRestLengthList = [0 for x in range(maxLevel)]
        # self.kList = [1 for x in range(2*maxLevel + 1)]
        # self.restLengthList = [0 for x in range(2*maxLevel + 1)]


# class Spring:
#     def __init__(self, k = 0):
#         self.direction = np.zeros(3)
#         self.length = 0
#         self.restLength = 0
#         self.k = k
        

windowWidth = 640
windowHeight = 480
class System:
    def __init__(self, n):
        self.elements = []
        self.n = n
        self.kList = np.array([[1, 2, 0, 2, 1] for x in range (self.n)])
        self.restLengthList = np.zeros((self.n, 2*maxLevel+1))
        self.accumilateTime = 0.0

        self.generate()

    def generate(self):
        # self.n = n
        for i in range(self.n):
            e = Element()
            e.position = np.array([windowWidth/2, i*30, 0], dtype = float)
            self.elements.append(e)

        # initialize rest length of springs
        for level in range(1, maxLevel + 1):
            for i in range(self.n - level):
                e = self.elements[i]
                eNext = self.elements[i + level]
                vec = eNext.position - e.position
                self.restLengthList[i][maxLevel + level] = self.restLengthList[i + level][maxLevel - level] = np.linalg.norm(vec)


    def animate(self, deltaT):
        self.accumilateTime += deltaT
        externalAcc = np.array([1, 9.8, 0])
        tempVelocitys = np.zeros((self.n, 3))
        tempPositions = np.zeros((self.n, 3))
        outfile.write("dT={:.3f}: ".format(deltaT))
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
            resultantAcc = resultantForce/e.mass
            resultantAcc += externalAcc
            resultantAcc += e.velocity*e.damping
            tempPositions[i] = e.position + (e.velocity + resultantAcc * deltaT / 2) * deltaT
            tempVelocitys[i] = e.velocity + resultantAcc * deltaT
            outfile.write("point{}:a={:7.3f}, p={:7.3f}, v={:7.3f}; ".format(i, resultantAcc[1], tempPositions[i][1], tempVelocitys[i][1]))
        outfile.write("\n")

        for i in range(1, self.n):
            self.elements[i].position = tempPositions[i]
            self.elements[i].velocity = tempVelocitys[i]

            


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.s = System(3)
        self.lastTime = time.time()
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process)
        self.timer.start(30)

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
            radius = 10
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


# class A:
#     def __init__(self, b):
#         self.b = b
#         self.b.add()
#         return
#     def add(self):
#         self.b.add()
# class B:
#     def __init__(self, *args, **kwargs):
#         self.value = 0
#         return super().__init__(*args, **kwargs)
#     def add(self):
#         self.value += 1
# b = B()
# a1 = A(b)
# a2 = A(b)
# print(b.value)
# print(a1.b.value)
# print(a2.b.value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())