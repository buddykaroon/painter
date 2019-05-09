from PyQt5.QtWidgets import QApplication , QMainWindow, QMenuBar, QMenu, QAction, QGraphicsItem, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QTabletEvent, QColor, QLinearGradient, QRegion
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
        self.image.fill(Qt.blue)
        self.imageAbove.fill(Qt.transparent)
        self.imageTemp.fill(Qt.transparent)
        self.baseSize = 2
        self.drawing = False
        self.brushSize = 15
        self.brushColor = (QColor(255, 0, 0, 50))
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
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        clearAction = QAction(QIcon("exit.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        clearAction.triggered.connect(self.clear)
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
        empty = QPoint(0,0)
        point2 = QPoint(100,100)
        point3 = QPoint(200,150)
        point4 = QPoint(300,175)
        point5 = QPoint(400,150)


        self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        self.line = QLine(empty, point2)

        painterTemp = QPainter(self.imageAbove)
        painterTemp.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painterTemp.setCompositionMode(QPainter.CompositionMode_SourceOver)
        self.line = QLine(point2, point3)
        painterTemp.drawLine(self.line)
        painterTemp.setCompositionMode(QPainter.CompositionMode_Source)
        painterTemp.setPen(QPen(Qt.transparent, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painterTemp.drawPoint(point3)
        painterTemp.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painterTemp.setCompositionMode(QPainter.CompositionMode_SourceOut)
        self.line = QLine(point3, point4)
        painterTemp.drawLine(self.line)
        painterTemp.setCompositionMode(QPainter.CompositionMode_SourceOut)
        self.line = QLine(point4, point5)
        painterTemp.drawLine(self.line)
        self.painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        self.painter.drawImage(empty, self.imageAbove)
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
            self.painter.drawImage(empty, self.imageTemp) #Draw save state
            self.painter.drawImage(empty, self.imageAbove)
            self.imageAbove.fill(Qt.transparent)
            self.strokeCount = 0
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
            # MAKESHIFT code that "fixes" the coder issue.
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            self.line = QLine(self.lastPoint, event.pos())
            painterTemp = QPainter(self.imageAbove)
            painterTemp.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            if (self.strokeCount == 0):
                painterTemp.setCompositionMode(QPainter.CompositionMode_SourceOver)
                painterTemp.drawLine(self.line)
                self.strokeCount = 1
            else:
                self.painterSim.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.painterSim.setCompositionMode(QPainter.CompositionMode_SourceOver)
                self.painterSim.drawLine(self.line)
                self.painterSim.setPen(QPen(Qt.transparent, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                self.painterSim.setCompositionMode(QPainter.CompositionMode_Source)
                self.painterSim.drawPoint(event.pos())

            self.brushColor = Qt.transparent
            self.painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painterTemp.end()
            empty = QPoint(0,0)
            self.painter.drawImage(empty, self.imageTemp)
            self.imageTemp.fill(Qt.transparent)
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.drawing = False
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
    def save(self):
        filePath, _= QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);; ALL File(*.*)")
        if filePath == "":
            return
        else:
            self.image.save(filePath)
    def clear(self):
        self.image.fill(Qt.white)
        self.imageTemp.fill(Qt.white)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()