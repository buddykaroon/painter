from PyQt5.QtWidgets import QApplication , QMainWindow, QMenuBar, QMenu, QAction, QGraphicsItem
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QTabletEvent, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, QLine
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 400
        left = 400
        width = 800
        height = 600
        icon = "web.png"
        self.setWindowTitle("Paint Application")
        self.setWindowIcon(QIcon(icon))
        self.setGeometry(top, left, width, height)
        self.imageTemp = QImage(self.size(), QImage.Format_ARGB32)
        self.imageAbove = QImage(self.size(), QImage.Format_ARGB32)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.imageAbove.fill(Qt.transparent)
        self.imageTemp.fill(Qt.transparent)
        self.baseSize = 2
        self.drawing = False
        self.brushSize = 15
        self.brushColor = (QColor(0, 0, 0, 0.01))
        self.lastPoint = QPoint()
        self.tempColor = QColor(0, 0, 0, 1)
        self.pen_pressure = 90
        self.strokeCount = 0
        self.line = QLine(0,0,1,1)
        self.painter = QPainter(self.image)
        self.painterSim = QPainter(self.imageTemp)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushMenu = mainMenu.addMenu("Brush Size")
        brushColor = mainMenu.addMenu("Brush Color")

        saveAction = QAction(QIcon("exit.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)

        clearAction = QAction(QIcon("exit.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)

        threepxAction = QAction(QIcon("exit.png"), "Three px", self)
        threepxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(threepxAction)
        sixpxAction = QAction(QIcon("exit.png"), "Six px", self)
        sixpxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(sixpxAction)
        ninepxAction = QAction(QIcon("exit.png"), "Nine px", self)
        ninepxAction.setShortcut("Ctrl+T")
        brushMenu.addAction(ninepxAction)

        blackAction = QAction(QIcon("exit.png"), "Black Color", self)
        blackAction.setShortcut("Ctrl+T")
        brushColor.addAction(blackAction)
        whiteAction = QAction(QIcon("exit.png"), "White Color", self)
        whiteAction.setShortcut("Ctrl+T")
        brushColor.addAction(whiteAction)
        redAction = QAction(QIcon("exit.png"), "Red Color", self)
        redAction.setShortcut("Ctrl+T")
        brushColor.addAction(redAction)

    def tabletEvent(self, tabletEvent):
        print("hello")
        self.pen_x = tabletEvent.globalX()
        self.pen_y = tabletEvent.globalY()
        self.pen_pressure = int(tabletEvent.pressure() * 100)
        self.brushColor = (QColor(0, 0, 0,  self.pen_pressure * 2.55))
        print(self.pen_pressure)
        if tabletEvent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            print("TabletPress event")
        elif tabletEvent.type() == QTabletEvent.TabletMove:
            self.pen_is_down = True
            print("TabletMove event")
        elif tabletEvent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            print("TabletRelease event")
            empty = QPoint(0,0)
            self.painter.drawImage(empty, self.imageTemp)
            self.painter.drawImage(empty, self.imageAbove)
            self.imageAbove.fill(Qt.transparent)
            self.painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            self.painter.drawImage(empty , self.image)
            self.painterSim.drawImage(empty, self.image) #Save state

        if self.pen_is_down:
            print(" Pen is down.")

        else:
            print(" Pen is up.")
        tabletEvent.accept()
        self.update()
    def mousePressEvent (self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            print(self.lastPoint)
    def mouseMoveEvent(self, event):
            # MAKESHIFT code that fixes the coder issue.
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            self.line = QLine(self.lastPoint, event.pos())
            painterTemp = QPainter(self.imageAbove)
            painterTemp.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painterTemp.setCompositionMode(QPainter.CompositionMode_Source)
            painterTemp.drawLine(self.line)
            self.painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painterTemp.end()
            empty = QPoint(0,0)
            self.painter.drawImage(empty, self.imageAbove)
            self.lastPoint = event.pos()
            self.update()
    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.drawing = False
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()