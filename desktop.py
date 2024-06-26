# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *
# import sys
# # from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import *
# # from PyQt5.QtCore import *


# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         if not MainWindow.objectName():
#             MainWindow.setObjectName(u"MainWindow")
#         MainWindow.resize(640, 480)
#         self.centralwidget = QWidget(MainWindow)
#         self.centralwidget.setObjectName(u"centralwidget")
#         self.horizontalLayoutWidget = QWidget(self.centralwidget)
#         self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
#         self.horizontalLayoutWidget.setGeometry(QRect(150, 10, 291, 41))
#         self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout.setObjectName(u"horizontalLayout")
#         self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
#         self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
#         self.pushButton_2.setObjectName(u"pushButton_2")
#         self.pushButton_2.setMaximumSize(QSize(120, 40))
#         font = QFont()
#         font.setFamily(u"Segoe Script")
#         font.setPointSize(12)
#         font.setBold(True)
#         font.setWeight(75)
#         self.pushButton_2.setFont(font)
#         self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))

#         self.horizontalLayout.addWidget(self.pushButton_2)

#         self.pushButton = QPushButton(self.horizontalLayoutWidget)
#         self.pushButton.setObjectName(u"pushButton")
#         self.pushButton.setMaximumSize(QSize(120, 40))
#         self.pushButton.setFont(font)
#         self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))

#         self.horizontalLayout.addWidget(self.pushButton)

#         self.pushButton_3 = QPushButton(self.centralwidget)
#         self.pushButton_3.setObjectName(u"pushButton_3")
#         self.pushButton_3.setGeometry(QRect(520, 400, 101, 41))
#         font1 = QFont()
#         font1.setFamily(u"SWItalt")
#         font1.setPointSize(12)
#         font1.setBold(True)
#         font1.setWeight(75)
#         self.pushButton_3.setFont(font1)
#         self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
#         self.pushButton_3.setAutoDefault(False)
#         self.pushButton_3.setFlat(False)
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.statusbar = QStatusBar(MainWindow)
#         self.statusbar.setObjectName(u"statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         self.retranslateUi(MainWindow)

#         self.pushButton_3.setDefault(False)


#         QMetaObject.connectSlotsByName(MainWindow)
#     # setupUi

#     def retranslateUi(self, MainWindow):
#         MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#         self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"BIOMETRIC", None))
#         self.pushButton.setText(QCoreApplication.translate("MainWindow", u"FACIAL", None))
#         self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Register", None))
#     # retranslateUi

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWindow = QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(mainWindow)
#     mainWindow.show()
#     sys.exit(app.exec_())


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(150, 10, 291, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMaximumSize(QSize(120, 40))
        font = QFont()
        font.setFamily("Segoe Script")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMaximumSize(QSize(120, 40))
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setGeometry(QRect(520, 400, 101, 41))
        font1 = QFont()
        font1.setFamily("SWItalt")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.pushButton_3.setFont(font1)
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.pushButton_3.setDefault(False)
        QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "SMART_ATTANDANCE", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "BIOMETRIC", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "FACIAL", None))
        # self.pushButton_2.connect.
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", "Register", None))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
