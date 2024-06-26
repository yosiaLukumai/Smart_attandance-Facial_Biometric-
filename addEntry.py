from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RegisterWindowDialog(object):
    def setupUi(self, RegisterWindow):
        if not RegisterWindow.objectName():
            RegisterWindow.setObjectName(u"RegisterWindow")
        RegisterWindow.resize(640, 480)
        RegisterWindow.setCursor(QCursor(Qt.PointingHandCursor))
        self.centralwidget = QWidget(RegisterWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(70, 350, 481, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamily(u"Cascadia Mono")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"color:#fff;\n""background-color:rgb(85, 0, 255);\n""border-radius:18;")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 70, 541, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:rgb(85, 0, 255);")

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        font1.setBold(True)
        font1.setItalic(True)
        font1.setWeight(75)
        self.lineEdit.setFont(font1)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 140, 231, 31))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color:rgb(85, 0, 255);")
        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(50, 170, 541, 42))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(0, 40))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QCursor(Qt.OpenHandCursor))
        self.pushButton_2.setStyleSheet(u"color:rgb(0, 170, 255)")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.label_3 = QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setWeight(75)
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color:rgb(255, 0, 255)")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(50, 240, 231, 31))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color:rgb(85, 0, 255);")
        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(50, 270, 541, 42))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget_3)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(0, 40))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setCursor(QCursor(Qt.OpenHandCursor))
        self.pushButton_3.setStyleSheet(u"color:rgb(0, 170, 255)")

        self.horizontalLayout_3.addWidget(self.pushButton_3)

        self.label_5 = QLabel(self.horizontalLayoutWidget_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 40))
        self.label_5.setFont(font2)
        self.label_5.setStyleSheet(u"color:rgb(255, 0, 255)")

        self.horizontalLayout_3.addWidget(self.label_5)

        RegisterWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(RegisterWindow)
        self.statusbar.setObjectName(u"statusbar")
        RegisterWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RegisterWindow)

        QMetaObject.connectSlotsByName(RegisterWindow)
    # setupUi

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QCoreApplication.translate("RegisterWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("RegisterWindow", u"SUBMIT", None))
        self.label.setText(QCoreApplication.translate("RegisterWindow", u"ENTER NAME", None))
        self.label_2.setText(QCoreApplication.translate("RegisterWindow", u"FINGERPRINT CONFIG", None))
        self.pushButton_2.setText(QCoreApplication.translate("RegisterWindow", u"CONNECT", None))
        self.label_3.setText(QCoreApplication.translate("RegisterWindow", u".", None))
        self.label_4.setText(QCoreApplication.translate("RegisterWindow", u"FACIAL REGISTRY", None))
        self.pushButton_3.setText(QCoreApplication.translate("RegisterWindow", u"CAPTURE", None))
        self.label_5.setText(QCoreApplication.translate("RegisterWindow", u".", None))

