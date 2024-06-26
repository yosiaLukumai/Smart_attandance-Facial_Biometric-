# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SmartAttandanceSthtNv.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(633, 460)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(150, 10, 291, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.Biometric = QPushButton(self.horizontalLayoutWidget)
        self.Biometric.setObjectName(u"Biometric")
        self.Biometric.setMaximumSize(QSize(120, 40))
        font = QFont()
        font.setFamily(u"Segoe Script")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Biometric.setFont(font)
        self.Biometric.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.Biometric)

        self.FacialButton = QPushButton(self.horizontalLayoutWidget)
        self.FacialButton.setObjectName(u"FacialButton")
        self.FacialButton.setMaximumSize(QSize(120, 40))
        self.FacialButton.setFont(font)
        self.FacialButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.FacialButton)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(520, 400, 101, 41))
        font1 = QFont()
        font1.setFamily(u"SWItalt")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.pushButton_3.setFont(font1)
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(90, 60, 431, 101))
        self.BiometricBox = QVBoxLayout(self.verticalLayoutWidget)
        self.BiometricBox.setObjectName(u"BiometricBox")
        self.BiometricBox.setContentsMargins(0, 0, 0, 0)
        self.fingerPrintSensor = QLabel(self.verticalLayoutWidget)
        self.fingerPrintSensor.setObjectName(u"fingerPrintSensor")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fingerPrintSensor.sizePolicy().hasHeightForWidth())
        self.fingerPrintSensor.setSizePolicy(sizePolicy)
        self.fingerPrintSensor.setMaximumSize(QSize(400, 40))
        font2 = QFont()
        font2.setFamily(u"MV Boli")
        font2.setPointSize(16)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.fingerPrintSensor.setFont(font2)
        self.fingerPrintSensor.setAlignment(Qt.AlignCenter)
        self.fingerPrintSensor.setMargin(0)

        self.BiometricBox.addWidget(self.fingerPrintSensor)

        self.FingerPrintSensor = QPushButton(self.verticalLayoutWidget)
        self.FingerPrintSensor.setObjectName(u"FingerPrintSensor")
        self.FingerPrintSensor.setMinimumSize(QSize(150, 40))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setWeight(75)
        self.FingerPrintSensor.setFont(font3)
        self.FingerPrintSensor.setCursor(QCursor(Qt.PointingHandCursor))
        self.FingerPrintSensor.setContextMenuPolicy(Qt.NoContextMenu)
        self.FingerPrintSensor.setLayoutDirection(Qt.LeftToRight)
        self.FingerPrintSensor.setAutoFillBackground(True)

        self.BiometricBox.addWidget(self.FingerPrintSensor)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(90, 170, 431, 191))
        self.FacialOptionBox = QGridLayout(self.gridLayoutWidget)
        self.FacialOptionBox.setObjectName(u"FacialOptionBox")
        self.FacialOptionBox.setContentsMargins(0, 0, 0, 0)
        self.picBox = QFrame(self.gridLayoutWidget)
        self.picBox.setObjectName(u"picBox")
        self.picBox.setFrameShape(QFrame.StyledPanel)
        self.picBox.setFrameShadow(QFrame.Sunken)

        self.FacialOptionBox.addWidget(self.picBox, 0, 0, 1, 2)

        self.CaptureButton = QPushButton(self.gridLayoutWidget)
        self.CaptureButton.setObjectName(u"CaptureButton")
        self.CaptureButton.setMaximumSize(QSize(120, 40))
        self.CaptureButton.setFont(font)
        self.CaptureButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.FacialOptionBox.addWidget(self.CaptureButton, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_3.setDefault(False)

        self.gridLayoutWidget.hide()

        self.Biometric.clicked.connect(self.showBiometricBox)
        self.FacialButton.clicked.connect(self.showFacialBox)


        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Biometric.setText(QCoreApplication.translate("MainWindow", u"BIOMETRIC", None))
        self.FacialButton.setText(QCoreApplication.translate("MainWindow", u"FACIAL", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.fingerPrintSensor.setText(QCoreApplication.translate("MainWindow", u"CONNECT TO FINGERPRINT", None))
        self.FingerPrintSensor.setText(QCoreApplication.translate("MainWindow", u"CONNECT", None))
        self.CaptureButton.setText(QCoreApplication.translate("MainWindow", u"CAPTURE", None))

    
    def showFacialBox(self):
        self.gridLayoutWidget.show()
        self.gridLayoutWidget.setGeometry(QRect(90, 60, 431, 191))
        self.verticalLayoutWidget.hide()
    
    def showBiometricBox(self):
        self.gridLayoutWidget.hide()
        self.verticalLayoutWidget.show()
        self.verticalLayoutWidget.setGeometry(QRect(90, 60, 431, 101))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
