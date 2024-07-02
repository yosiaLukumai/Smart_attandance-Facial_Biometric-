import face_recognition
import cv2
import pickle
import atexit
import numpy as np

dataset_path = "datasets/"
TherePicToProcess = False


camera = cv2.VideoCapture(0)
frame_width = 320
frame_height = 240
camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

def housecleanup():
    print("__SOME HOUSE CLEANING__")
    # if TherePicToProcess:
    #     passImage()
    #     time.sleep(2)

    cv2.destroyAllWindows()
    camera.release()

atexit.register(housecleanup)

def passImage():
    # unknown_image = face_recognition.load_image_file("io.jpg")
    face_locations = face_recognition.face_locations()
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_names[best_match_index]
        

        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.rectangle(unknown_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(unknown_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        cv2.imshow("Image", unknown_image)
           


# while True:
#     ret, frame = camera.read()
#     if not ret:
#         print("failed to grab frame")
#         break
#     cv2.imshow("press space to take a photo", frame)

#     k = cv2.waitKey(1)
#     if k%256 == 27:
#         print("Escape hit, closing...")
#         break
#     elif k%256 == 32:
#         written = cv2.imwrite("workingImage.jpg", frame)
#         print(written)
#         break




while True:
    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break
    else:
        detected = False
        unknown_image = np.array(frame)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            confidence = 1 - face_distances[best_match_index]
            #print("Confidence:  ", confidence)
            #print("Name: ", name)
            if matches[best_match_index] and confidence > 0.6:
                name = known_names[best_match_index]
            
            cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(unknown_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(unknown_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
        cv2.imshow("Image", unknown_image)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            print("------EXITING---------")
            break
    






