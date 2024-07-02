from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2
import numpy as np
import atexit
import face_recognition
import pickle

dataset_path = "datasets/" 
with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Results")
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        self.label = QLabel("Name: ")
        layout.addWidget(self.label)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)

    def center(self, parent):
        parent_geometry = parent.geometry()
        parent_center = parent_geometry.center()
        self_geometry = self.geometry()
        self_geometry.moveCenter(parent_center)
        self.setGeometry(self_geometry)
    
    def setTextResult(self, name):
        self.label.setText(f"{name}")


class Worker1(QThread):
    ImageUpdate = Signal(QImage)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ThreadActive = False
        self.currentFrame = None

    def run(self):
        self.ThreadActive = True
        self.Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = self.Capture.read()
            self.currentFrame = frame
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        self.Capture.release()

    def stop(self):
        self.ThreadActive = False
        self.wait()  # Wait for the thread to finish


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(514, 440)
        MainWindow.setMinimumSize(QSize(514, 420))
        MainWindow.setMaximumSize(QSize(514, 420))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(100, 10, 291, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.FacialButton = QPushButton(self.horizontalLayoutWidget)
        self.FacialButton.setObjectName(u"FacialButton")
        self.FacialButton.setMaximumSize(QSize(300, 40))
        font = QFont()
        font.setFamily(u"Segoe Script")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.FacialButton.setFont(font)
        self.FacialButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.FacialButton.setStyleSheet(u"color:rgb(85, 85, 255)")

        self.horizontalLayout.addWidget(self.FacialButton)

        self.CaptureButton = QPushButton(self.centralwidget)
        self.CaptureButton.setObjectName(u"CaptureButton")
        self.CaptureButton.setGeometry(QRect(180, 350, 120, 35))
        self.CaptureButton.setMaximumSize(QSize(120, 40))
        self.CaptureButton.setFont(font)
        self.CaptureButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CaptureButton.setStyleSheet(u"color:rgb(255, 0, 127);")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 70, 320, 240))
        self.label.setMinimumSize(QSize(320, 240))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.tmp = None

        # Modes for the
        self.FacialMode = False
        self.dialogResult = MyDialog()
        self.CaptureButton.clicked.connect(self.showDialog)
        self.FacialRecognized = False
        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.start()

    def closeEvent(self, event):
        self.Worker1.stop()
        event.accept()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Smart Door", None))
        self.FacialButton.setText(QCoreApplication.translate("MainWindow", u"SMART DOOR", None))
        self.CaptureButton.setText(QCoreApplication.translate("MainWindow", u"CAPTURE", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"l", None))

    def cleanupResources(self):
        self.Worker1.stop()

    def showFacialBox(self):
        self.Worker1.start()
    
    def ImageUpdateSlot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.stop()
    
    def showDialog(self):
        self.passImage()
        self.dialogResult.center(mainWindow)
        self.dialogResult.exec_()
    
    def passImage(self):
        unknown_image = np.array(self.Worker1.currentFrame).astype("uint8")
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

            print(name)
            self.FacialRecognized = True
            try:
                if self.Worker1.currentFrame is None:
                    self.dialogResult.setTextResult("Re-try failed to fetch")
                else:
                    self.dialogResult.setTextResult("Name: " + name)
            except Exception as e:
                print("Error in setting the result")
                print(e)

        if not self.FacialRecognized:
            self.dialogResult.setTextResult("Name: Unknown")
        
        self.FacialRecognized = False


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    atexit.register(ui.cleanupResources)

    sys.exit(app.exec_())
