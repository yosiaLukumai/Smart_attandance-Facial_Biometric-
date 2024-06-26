import face_recognition
import cv2
import pickle
import numpy as np

dataset_path = "datasets/"
TherePicToProcess = False


camera = cv2.VideoCapture(0)
frame_width = 640
frame_height = 480
camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

def housecleanup():
    print("____")
    # if TherePicToProcess:
    #     passImage()
    #     time.sleep(2)

    cv2.destroyAllWindows()
    camera.release()

# atexit.register(housecleanup)

def passImage():
    unknown_image = face_recognition.load_image_file("io.jpg")
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

camera.release()
cv2.destroyAllWindows()



unknown_image = face_recognition.load_image_file("workingImage.jpg")
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
    cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.rectangle(unknown_image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(unknown_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # if cv2.waitKey(1) & 0xFF == ord('q'): 
    #             print("---------------")
    #             break
    



cv2.imshow("Image", unknown_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



