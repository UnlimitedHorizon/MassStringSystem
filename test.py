import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import numpy as np


maxLevel = 2
class Element:
    def __init__(self):
        self.mass = 0
        self.damping = 0

        self.position = np.zeros(3)
        self.lastPostion = np.zeros(3)

        self.velocity = np.zeros(3)

        self.kList = [0 for x in range(2*maxLevel + 1)]
        self.restLengthList = [0 for x in range(2*maxLevel + 1)]
        self.preElement = None
        self.nextElement = None

        self.preString = None
        self.nextString = None

        self.preString2 = None
        self.nextString2 = None


# class Spring:
#     def __init__(self, k = 0):
#         self.direction = np.zeros(3)
#         self.length = 0
#         self.restLength = 0
#         self.k = k
        

windowWidth = 640
windowHeight = 480
class System:
    def __init__(self):
        self.elements = []
        self.strings = []
        self.n = 0

    def generate(self, n):
        self.n = n
        for i in range(n):
            e = Element()
            e.position = np.array([windowWidth/2, i*100, 0], dtype = float)
            self.elements.append(e)

        for level in range(1, maxLevel + 1):
            for i in range(n - level):
                e = self.elements[i]
                eNext = self.elements[i + level]
                vec = eNext.position - e.position
                e.restLengthList[maxLevel - 1 + level] = eNext.restLengthList[maxLevel + 1 - level] = np.linalg.norm(vec)

        # s = Spring()                
        # for i in range(n-1):
        #     e = self.elements[i]
        #     eNext = self.elements[i+1]
        #     vec = eNext - e
        #     s.restLength = np.linalg.norm(vec)
        #     s.length = s.restLength



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.s = System()
        self.s.generate(3)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, windowWidth, windowHeight)
        self.setWindowTitle("Test")
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        # self.drawPoints(qp)
        self.drawSystem(qp)
        qp.end()

    def drawSystem(self, qp):
        elements = self.s.elements
        eLast = None
        for e in elements:
            qp.setPen(QPen(Qt.blue, 4, Qt.SolidLine));
            radius = 10
            qp.drawEllipse(e.position[0], windowHeight - e.position[1], 10, 10);
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