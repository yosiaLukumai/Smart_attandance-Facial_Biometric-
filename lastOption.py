import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWin(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWin, self).__init__(*args, **kwargs)
        self.Label = QPushButton()
        self.setWindowTitle("Smart Attandance [SA]")
        self.setFixedSize(QSize(900, 600))
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#4CC9F0"))
        self.setPalette(palette)

        # Adding the Header of the application
        self.mainAppLayout = QGridLayout()
        self.appLabel = QLabel("Smart Attandance [SA]")
        # self.mainAppLayout.setAlignment(self.appLabel, Qt.AlignVCenter)
        self.appLabel.setFixedHeight(30)
        self.appLabel.setFont(QFont("Serif", 25, 20))
        
        # formating text size and position

        self.mainAppLayout.addWidget(self.appLabel, 0, 1, Qt.AlignTop)

        # Adding the Buttons

        self.MenuSelector = QHBoxLayout()
        self.MainAppContent = QVBoxLayout()
        self.MainResult = QVBoxLayout()
        self.RegisterButton = QHBoxLayout()


        self.FacialSelection = QPushButton("Facial")
        self.FingerSearchTab = QPushButton("Biometeric")
        self.FingerSearchTab.setFixedSize(QSize(190, 50))
        self.FacialSelection.setFixedSize(QSize(120, 50))
        self.FacialSelection.setFont(QFont("Serif", 25, 20))
        self.FingerSearchTab.setFont(QFont("Serif", 25, 20))
        self.MenuSelector.addWidget(self.FacialSelection)
        self.MenuSelector.addWidget(self.FingerSearchTab)
        self.mainAppLayout.addLayout(self.MenuSelector, 1,1, Qt.AlignTop)

        self.RegisB = QPushButton("Register")
        self.RegisB.setFixedSize(QSize(190, 50))
        self.RegisB.setFont(QFont("Serif", 25, 20))
        self.mainAppLayout.addWidget(self.RegisB, 2, 1)
        self.mainAppLayout.addLayout(self.RegisterButton, 2, 2)
        #attaching the Widgets onto the window..
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainAppLayout)
        self.setCentralWidget(self.mainWidget)

    def mousepressEvent(self, e):
        print("called...")
    def listenClicks(self):
        print("clicked...")

    def listenToggle(self, checkM):
        print("==", checkM)


app = QApplication(sys.argv)

wind = MainWin()
wind.show()

app.exec_()