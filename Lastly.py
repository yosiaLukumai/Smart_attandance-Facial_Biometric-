from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
import numpy as np
from picamera2 import Picamera2
import atexit
import face_recognition
import pickle
import time
import serial
import adafruit_fingerprint
import csv
filename = "fingerPrints.csv"


def read_csv_to_dict(filename):
    data_dict = {}
    last_id = 0
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_dict[row['id']] = row['name']
                last_id = max(last_id, int(row['id']))
    except FileNotFoundError:
        pass  # If the file doesn't exist, start with an empty dictionary
    return data_dict, last_id

def write_dict_to_csv(filename, data_dict):
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id, name in data_dict.items():
            writer.writerow({'id': id, 'name': name})

def update_or_add_entry(filename, id_to_update, new_name):
    data_dict, last_id = read_csv_to_dict(filename)
    
    if id_to_update in data_dict:
        data_dict[id_to_update] = new_name  # Update existing entry
    else:
        new_id = str(last_id + 1)
        data_dict[new_id] = new_name  # Add new entry
    
    write_dict_to_csv(filename, data_dict)

def find_name_by_id(filename, id_to_find):
    data_dict, _ = read_csv_to_dict(filename)
    return data_dict.get(id_to_find, "ID not found")

def is_name_taken(filename, name_to_check):
    data_dict, _ = read_csv_to_dict(filename)
    return name_to_check in data_dict.values()

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
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.currentFrame = None
        self.ThreadActive = True
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)}))
        picam2.start()
        while self.ThreadActive:
            frame = picam2.capture_array()
            self.currentFrame = frame
            if True:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()
    
    def currentFrame(self):
        return self.currentFrame
    


class WorkerFingerRegister(QThread):
    RegistrationResults = pyqtSignal(bool)
    ProcessInfo = pyqtSignal(str)
    def run(self):
        self.ThreadActive = True
        try:
            uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
            self.finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

            # let try to get the index of the finger_print
            _, last_id = read_csv_to_dict(filename) + 1
            last_id = int(last_id) + 1
            flag = self.enroll_finger(last_id)
            if flag:
                print("************************* All went welll **************")
                self.ProcessInfo.emit(" Well set OK..")
                self.RegistrationResults.emit(True)
            else:
                self.ProcessInfo.emit(f"Error:  Failed retry")
                self.RegistrationResults.emit(False)
        except Exception as e:
            self.ProcessInfo.emit(f"Error: {str(e)}")
            self.RegistrationResults.emit(False)
    

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def enroll_finger(self, location):
        """Take a 2 finger images and template it, then store in 'location'"""
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                self.ProcessInfo.emit("Place finger on sensor...")
                print("Place finger on sensor...", end="")
            else:
                self.ProcessInfo.emit("Place same finger again...")
                print("Place same finger again...", end="")

            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    print("Image taken")
                    self.ProcessInfo.emit("Image Taken")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    print(".", end="")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    self.ProcessInfo.emit("Error:  Imaging error (Re-try..)")
                    print("Imaging error")
                    return False
                else:
                    print("Other error")
                    return False
            print("Templating...", end="")
            i = self.finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                print("Templated")
            else:

                if i == adafruit_fingerprint.IMAGEMESS:
                    self.ProcessInfo.emit("Error:  Image too messy (Re-try..)")
                    print("Image too messy")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    self.ProcessInfo.emit("Error: Could not identify features (Re-try..)")
                    print("Could not identify features")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    print("Image invalid")
                    self.ProcessInfo.emit("Error: Image invalid (Re-try..)")
                else:
                    self.ProcessInfo.emit("Error: Unknown (Re-try..)")
                    print("Other error")
                return False

            if fingerimg == 1:
                self.ProcessInfo.emit("Remove finger")
                print("Remove finger")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()

        print("Creating model...", end="")
        i = self.finger.create_model()
        if i == adafruit_fingerprint.OK:
            print("Created")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                self.ProcessInfo.emit("Error: Prints did not match (Re-try..)")
                print("Prints did not match")
            else:
                self.ProcessInfo.emit("Error: Unknown (Re-try..)")
                print("Other error")
            return False

        print("Storing model #%d..." % location, end="")
        i = self.finger.store_model(location)
        if i == adafruit_fingerprint.OK:
            print("Stored")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                print("Bad storage location")
            elif i == adafruit_fingerprint.FLASHERR:
                print("Flash storage error")
            else:
                print("Other error")
            return False
        
        return True


class Worker2(QThread):
    FingerPrintUpdate = pyqtSignal(str)
    ProcessCont = pyqtSignal(str)
    def run(self):
        self.ThreadActive = True
        try:
            f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                   self.FingerPrintUpdate.emit("0-Failed to Initialize")
                # raise ValueError('The given fingerprint sensor password is wrong!')
            self.ProcessCont.emit("===CONNECTED====")
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            self.FingerPrintUpdate.emit("0-Failed to Initialize")
        ## Gets some sensor information

        try:
            print('Waiting for finger...')
            self.ProcessCont.emit("Waiting for finger...")
            ## Wait that finger is read
            while ( f.readImage() == False ) and self.ThreadActive:
                pass

            f.convertImage(FINGERPRINT_CHARBUFFER1)

            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                self.FingerPrintUpdate.emit("0-None")  

            else:
                print('Found template at position #' +  str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))
                self.FingerPrintUpdate.emit("1-"+  str(positionNumber))



        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            self.FingerPrintUpdate.emit("0-Something Went Wrong" + str(e))  
                
    def stop(self):
        self.ThreadActive = False
        self.quit()
    
    


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(633, 460)
        MainWindow.setStyleSheet(u"")
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
        self.Biometric.setStyleSheet(u"color:rgb(85, 170, 255);")

        self.horizontalLayout.addWidget(self.Biometric)

        self.FacialButton = QPushButton(self.horizontalLayoutWidget)
        self.FacialButton.setObjectName(u"FacialButton")
        self.FacialButton.setMaximumSize(QSize(120, 40))
        self.FacialButton.setFont(font)
        self.FacialButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.FacialButton.setStyleSheet(u"color:rgb(85, 170, 255);")

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
        self.pushButton_3.setStyleSheet(u"color:rgb(255, 0, 127);")
        self.pushButton_3.setAutoDefault(False)
        self.pushButton_3.setFlat(False)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(90, 60, 431, 81))
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
        self.fingerPrintSensor.setMaximumSize(QSize(430, 40))
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
        font3.setFamily(u"Segoe Script")
        font3.setPointSize(14)
        font3.setBold(True)
        font3.setWeight(75)
        self.FingerPrintSensor.setFont(font3)
        self.FingerPrintSensor.setCursor(QCursor(Qt.PointingHandCursor))
        self.FingerPrintSensor.setContextMenuPolicy(Qt.NoContextMenu)
        self.FingerPrintSensor.setLayoutDirection(Qt.LeftToRight)
        self.FingerPrintSensor.setAutoFillBackground(False)
        self.FingerPrintSensor.setStyleSheet(u"color:rgb(255, 0, 127);")

        self.BiometricBox.addWidget(self.FingerPrintSensor)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(90, 140, 431, 291))
        self.FacialOptionBox = QGridLayout(self.gridLayoutWidget)
        self.FacialOptionBox.setObjectName(u"FacialOptionBox")
        self.FacialOptionBox.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(320, 240))

        self.FacialOptionBox.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(200, 170, 251, 71))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(12)
        font4.setBold(True)
        font4.setItalic(True)
        font4.setWeight(75)
        self.label_2.setFont(font4)

        self.CaptureButton = QPushButton(self.gridLayoutWidget)
        self.CaptureButton.setObjectName(u"CaptureButton")
        self.CaptureButton.setMaximumSize(QSize(120, 40))
        self.CaptureButton.setFont(font)
        self.CaptureButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.CaptureButton.setStyleSheet(u"color:rgb(255, 0, 127);")

        self.FacialOptionBox.addWidget(self.CaptureButton, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton_3.setDefault(False)

        QMetaObject.connectSlotsByName(MainWindow)
        self.gridLayoutWidget.hide()

        self.Biometric.clicked.connect(self.showBiometricBox)
        self.FacialButton.clicked.connect(self.showFacialBox)
        self.tmp = None

        #modes for the 
        self.FacialMode = False
        self.Worker1 = Worker1()
        self.Worker2 = Worker2()
        self.dialogResult = MyDialog()
        self.FingerResultsDialog = MyDialog()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker2.ProcessCont.connect(self.processOngoing)
        self.Worker2.FingerPrintUpdate.connect(self.FingerPrintResultSlot)
        self.CaptureButton.clicked.connect(self.showDialog)
        self.FacialRecognized = False
        self.pushButton_3.clicked.connect(self.showRegisterDialog)
        self.FingerPrintSensor.clicked.connect(self.StartFingerprintScanning)

        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Biometric.setText(QCoreApplication.translate("MainWindow", u"BIOMETRIC", None))
        self.FacialButton.setText(QCoreApplication.translate("MainWindow", u"FACIAL", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.fingerPrintSensor.setText(QCoreApplication.translate("MainWindow", u"CONNECT TO FINGERPRINT", None))
        self.FingerPrintSensor.setText(QCoreApplication.translate("MainWindow", u"CONNECT", None))
        self.label.setText("")
        self.label_2.setText("")
        self.CaptureButton.setText(QCoreApplication.translate("MainWindow", u"CAPTURE", None))
    # retranslateUi

    def cleanupResources(self):
        print("cleaning up resources....")
        self.Worker1.stop()
        self.Worker2.stop()

    def processOngoing(self, msg):
        self.label_2.setText(msg)

    def showFacialBox(self):
        self.gridLayoutWidget.show()
        self.gridLayoutWidget.setGeometry(QRect(90, 60, 431, 280))
        self.verticalLayoutWidget.hide()
        self.FacialMode = True
        self.Worker1.start()

    
    def ImageUpdateSlot(self, Image):
        self.label.setPixmap(QPixmap.fromImage(Image))

    def FingerPrintResultSlot(self, Result:str):
        results = Result.split("-")
        if(results[0] == '1'):
            print("Id found:  "+ str(results[1]))
            name = find_name_by_id(filename, results[1])
            self.FingerResultsDialog.setTextResult(f"Name: {name}")

        else:
            if results[1] == "None":
                print("No match found")
                self.FingerResultsDialog.setTextResult("No match found")
            else:
                print("Other result: ", results[1])
                self.FingerResultsDialog.setTextResult(results[1])
        self.Worker2.stop()

        #Bring dialog forth
        self.showDialogFingerResult()
    
    def StartFingerprintScanning(self):
        self.Worker2.start()



 
    def CancelFeed(self):
        self.Worker1.stop()

    
    def showBiometricBox(self):
        self.Worker1.stop()
        self.FacialMode = False
        self.gridLayoutWidget.hide()
        self.verticalLayoutWidget.show()
        self.verticalLayoutWidget.setGeometry(QRect(90, 60, 431, 101))

    def showDialogFingerResult(self):
        self.FingerResultsDialog.center(mainWindow)
        self.FingerResultsDialog.exec_()

    def showDialog(self):
        self.passImage()
        self.dialogResult.center(mainWindow)
        self.dialogResult.exec_()

    def showRegisterDialog(self):
        # self.register_window = RegisterWindow(self)
        # self.register_window.show()
        self.window = QMainWindow()
        self.ui = RegisterWindow(self.window)
        self.ui.exec()
        
    
    def passImage(self):
        unknown_image = np.array(self.Worker1.currentFrame).astype("uint8")
        unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

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

            # cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

            # cv2.rectangle(unknown_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            # font = cv2.FONT_HERSHEY_DUPLEX
            # cv2.putText(unknown_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # cv2.imshow("Image", unknown_image)
        if self.FacialRecognized == False:
            self.dialogResult.setTextResult("Name: " +"Unknown")
        
        self.FacialRecognized = False

class Ui_RegisterWindow(object):
    def setupUi(self, RegisterWindow):
        if not RegisterWindow.objectName():
            RegisterWindow.setObjectName(u"RegisterWindow")
        RegisterWindow.resize(640, 480)
        RegisterWindow.setCursor(QCursor(Qt.PointingHandCursor))
        self.centralwidget = QWidget(RegisterWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(70, 340, 481, 51))
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
        self.label_4.setGeometry(QRect(50, 240, 501, 41))
        font3 = QFont()
        font3.setFamily(u"Sitka Subheading")
        font3.setPointSize(16)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setWeight(50)
        self.label_4.setFont(font3)

        # RegisterWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QStatusBar(RegisterWindow)
        # self.statusbar.setObjectName(u"statusbar")
        # RegisterWindow.setStatusBar(self.statusbar)


        # code handling
        self.BiometricSuccesful = False
        self.dialogResult = MyDialog()

        self.retranslateUi(RegisterWindow)

        self.pushButton.clicked.connect(self.submitRegistration)
        self.pushButton_2.clicked.connect(self.triggerBiometricRegistration)
        self.RegisterWorker = WorkerFingerRegister()
        self.RegisterWorker.RegistrationResults.connect(self.RegMainRes)
        self.RegisterWorker.ProcessInfo.connect(self.MainProcessRes)

        QMetaObject.connectSlotsByName(RegisterWindow)
    # setupUi

    def retranslateUi(self, RegisterWindow):
        RegisterWindow.setWindowTitle(QCoreApplication.translate("RegisterWindow", u"   RegisterWindow", None))
        self.pushButton.setText(QCoreApplication.translate("RegisterWindow", u"SUBMIT", None))
        self.label.setText(QCoreApplication.translate("RegisterWindow", u"ENTER NAME", None))
        self.label_2.setText(QCoreApplication.translate("RegisterWindow", u"FINGERPRINT CONFIG", None))
        self.pushButton_2.setText(QCoreApplication.translate("RegisterWindow", u"CONNECT", None))
        self.label_3.setText(QCoreApplication.translate("RegisterWindow", u".", None))
        self.label_4.setText("")

    def RegMainRes(self, flag:bool):
        if flag:
            self.BiometricSuccesful = True
        else:
            self.BiometricSuccesful = False

    def MainProcessRes(self, msg):
        self.label_4.setText(msg)

    def submitRegistration(self):
        if(self.lineEdit.text() != "" and self.BiometricSuccesful):
            print("We can close this sheet right now")
            _, last_id = read_csv_to_dict(filename)
            last_id = str(int(last_id) + 1)
            update_or_add_entry(filename, last_id, self.lineEdit.text())
            self.dialogResult.setTextResult("Successful registered Biometrics")
            self.dialogResult.center(mainWindow)
            self.dialogResult.exec_()

        else:
            if(self.lineEdit.text() == ""):
                self.dialogResult.setTextResult("Error:  Fill first name")
            else:
                self.dialogResult.setTextResult("Error: Register the Fingerprint First")
            self.dialogResult.center(mainWindow)
            self.dialogResult.exec_()
        
    def triggerBiometricRegistration(self):
        if(self.lineEdit.text() != ""):
            print(" Checking availabilty of the name")
            if not is_name_taken(filename, self.lineEdit.text()):
                print(" Let's try registering")
                self.RegisterWorker.start()
            else:
                print("  == NAME TAKEN === ")
                self.dialogResult.setTextResult("Error:   == NAME TAKEN === ")
                self.dialogResult.center(mainWindow)
                self.dialogResult.exec_()
        else:
            self.dialogResult.setTextResult("Error:   == FILL FIRST NAME === ")
            self.dialogResult.center(mainWindow)
            self.dialogResult.exec_()



      
class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    atexit.register(ui.cleanupResources)

    sys.exit(app.exec_())
