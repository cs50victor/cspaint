"""
- @author: Victor Atasie
- Paint Application
- Usability Testing
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QDesktopWidget, QAction, QFileDialog, QMessageBox, QColorDialog, \
    QPushButton, QToolBar, QLabel
from PyQt5.QtGui import QPainter, QCursor, QPen, QIcon, QImage, QFont
from PyQt5.QtCore import Qt, QPoint, QSize
from nPredictor import startPrediction


class CSPaint(QMainWindow):
    # noinspection SpellCheckingInspection
    def __init__(self):
        # required line of code for __init__ functions
        super().__init__()
        # a window is a defined visual space used to display our app.
        # window name
        self.setWindowTitle("CSPaint (Digit Predictor)")
        # using window icon gotten from flaticon.com
        self.setWindowIcon(QIcon("paint.png"))
        # fixed window size (width, height)
        self.setFixedSize(800, 800)
        self.frameGeometry().moveCenter(
            QDesktopWidget().availableGeometry().center())
        # creating a canvas for painting
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        self.image.fill(Qt.black)
        # to track drawing Points
        self.lastPoint = QPoint()
        # creating a default button style
        defaultButtonStyle = "QPushButton {border-radius:5px; border: 1px solid black;" \
                             " border-style: outset; min-width:20px;" \
                             "padding: 5px; margin:0 3px 7px 2px; color: 	#383838} " \
                             "QPushButton::hover:!pressed { color : black;}" \
                             "QMenu::item:selected {background-color: #7CB9E8;}"
        self.setStyleSheet(defaultButtonStyle)
        # important buttons for the toolBar
        # creating the brushColor button and giving it an icon
        self.changeBrushColor = QAction(QIcon("colorcircle.jpg"), "Brush Color", self)
        self.changeBrushColor.triggered.connect(self.colorPicker)
        self.changeBrushColor.setStatusTip("Brush Color")
        # creating the clearcanvas button
        self.clearButton = QPushButton("&Clear Canvas")
        self.clearButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.clearButton.setFont(QFont("Helvetica", 9, QFont.Medium))
        self.clearButton.clicked.connect(self.wipeOutEverything)
        # creating the predict Writing button
        self.predict = QPushButton("&Predict")
        self.predict.setFont(QFont("Helvetica", 9, QFont.Medium))
        self.predict.setCursor(QCursor(Qt.PointingHandCursor))
        self.predict.clicked.connect(self.predictNumber)
        # prediction text
        self.predictedNumber = QLabel("Current Prediction:\n --")
        self.predictedNumber.setFont(QFont("Helvetica", 9, QFont.Medium))
        self.predictedNumber.setStyleSheet("border-radius:2px; color: white; "
                              "background:black;")
        self.drawingInstructions = QLabel("\n\nINSTRUCTION:\nDraw a reasonably \n"
                                          "scaled digit (0-9) \nwithin the dotted \n"
                                          "square and click\n"
                                          "the Predict button.")
        self.drawingInstructions.setFont(QFont("Helvetica", 9, QFont.Medium))
        # default user controlled variables' values
        self.drawing = False
        self.brushSize = 5
        self.brushColor = Qt.white
        # open the file to store the user's mouseEvents
        self.data = open("mouseEvents.txt", "w")

        self.menuAndToolbar()

    # creating the menu bar
    def menuAndToolbar(self):
        appMenu = self.menuBar()
        appMenu.setStyleSheet("border-bottom:1px solid gray; color: #303030; "
                              "background:#F0F0F0;")
        appMenu.setFont(QFont("Helvetica", 12, QFont.Medium))
        # Using a QToolBar object
        # creating our toolbar area and adding button(widgets) to the toolbar
        moreFunctionToolBar = QToolBar("Functions", self)
        moreFunctionToolBar.setMovable(False)
        moreFunctionToolBar.setIconSize(QSize(70, 70))
        moreFunctionToolBar.setStyleSheet("border-right:2px solid gray;"
                                          " padding:8px 4px; background: white")
        self.addToolBar(Qt.LeftToolBarArea, moreFunctionToolBar)
        moreFunctionToolBar.addAction(self.changeBrushColor)
        moreFunctionToolBar.addWidget(self.clearButton)
        moreFunctionToolBar.addWidget(self.predict)
        moreFunctionToolBar.addWidget(self.predictedNumber)
        moreFunctionToolBar.addWidget(self.drawingInstructions)

        # adding menus and actions to our menuBar
        fileMenu = appMenu.addMenu(" File ")
        brushSize = appMenu.addMenu(" Brush Size ")
        saveCanvas = QAction("Save", self)
        saveCanvas.setShortcut("Ctrl+S")
        saveCanvas.triggered.connect(self.saveImage)
        lighter = QAction("1px", self)
        lighter.triggered.connect(self.lighterBrush)
        light = QAction("3px", self)
        light.triggered.connect(self.lightBrush)
        normal = QAction("5px", self)
        normal.triggered.connect(self.defaultBrush)
        bold = QAction("7px", self)
        bold.triggered.connect(self.boldBrush)
        bolder = QAction("9px", self)
        bolder.triggered.connect(self.bolderBrush)
        # adding all the actions to their respective menu buttons
        # file -> save
        # brush size -> lighter to bolder
        fileMenu.addAction(saveCanvas)
        brushSize.addAction(lighter)
        brushSize.addSeparator()
        brushSize.addAction(light)
        brushSize.addSeparator()
        brushSize.addAction(normal)
        brushSize.addSeparator()
        brushSize.addAction(bold)
        brushSize.addSeparator()
        brushSize.addAction(bolder)

    def lighterBrush(self):
        self.brushSize = 1

    def lightBrush(self):
        self.brushSize = 3

    def defaultBrush(self):
        self.brushSize = 5

    def boldBrush(self):
        self.brushSize = 7

    def bolderBrush(self):
        self.brushSize = 9

    # allows user to picker a brush color
    def colorPicker(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.brushColor = color

    def predictNumber(self):
        userFilePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "JustClickSave.jpg",
                                                      "JPEG(*.jpg *.jpeg);PNG(*.png);;All Files(*.*) ")

        if userFilePath == "":
            return
        else:
            self.image.save(userFilePath)
            startPrediction()

            with open("prediction.txt") as f:
                prediction = f.readline()

            if len(prediction) > 0:
                self.predictedNumber.setText("Current Prediction\n                "
                                             + str(prediction))
            else:
                self.predictedNumber.setText(""
                                             "ERROR!\n- To increase the prediction"
                                             "accuracy: \n1)use the 5px brush size\n"
                                             "2) Make sure drawing is scaled to fill the dotted square.\n"
                                             "3) Make sure you only clicked 'Save' when the dialog appears")

            # clears the canvas

    def wipeOutEverything(self):
        self.image.fill(Qt.black)
        self.update()

    # allows the user to save current drawing
    def saveImage(self):
        userFilePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                      "JPEG(*.jpg *.jpeg);PNG(*.png);;All Files(*.*) ")
        if userFilePath == "":
            return
        else:
            self.image.save(userFilePath)

    # allows the user to draw on canvas when the left button is clicked
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.data.write("x: %d y: %d\n" % (event.pos().x(), event.pos().y()))

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.data.write("x:%d y:%d\n" % (event.pos().x(), event.pos().y()))
            self.update()

    # disables drawing when the left is released
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter()
        pen = QPen(Qt.white, 1, Qt.DashLine)
        canvasPainter.begin(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        canvasPainter.setPen(pen)
        canvasPainter.drawRect(290, 290, 250, 250)
        canvasPainter.end()

    # function for telling the users they about to close the app
    def closeEvent(self, event):
        exit_msg = "Are you sure you want to exit the program?\n" \
                   "All unsaved work would be lost."
        reply = QMessageBox.question(self, 'Message',
                                     exit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.data.close()
        else:
            event.ignore()


def main():
    # creating the Painter application
    app = QApplication(sys.argv)
    # creating an instance of our app window
    window = CSPaint()
    # showing the window
    window.show()
    # starting/executing the CSPaint application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

"""
    1) Fixed window size (a user should not able to able to resize the window) 
                    [Done]
    2) Saving a painting as an image (through a QFileDialog)  
                [Done -> def saveImage]
    3) Color painting 
                [Done ]
    4) Painting with different brush sizes 
                [Done]
    5) Painting with different brush colors 
                [Done]
    6) Clearing a canvas with or without saving a painting 
                [Done-> def wipeOutEverything]
    7) Storing the mouse coordinates in a file while painting
                [Done]
"""
