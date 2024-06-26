from pathlib import Path
import face_recognition
import pickle
from PIL import Image
import time
import numpy as np
import atexit
import cv2
from collections import Counter
from tqdm import tqdm

  
fontScale = 1
color = (0, 250, 0) 
thickness = 2

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)
Path("validation").mkdir(exist_ok=True)

def encode_known_faces(model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH, training_dir: Path = Path("training")) -> None:
    names = []
    encodings = []
    for filepath in tqdm(training_dir.glob("*/*"), desc="Processing images"):
        name = filepath.parent.name
        print(filepath)
        try:
            image = face_recognition.load_image_file(filepath)
            face_locations = face_recognition.face_locations(image.astype("uint8"), model=model)
            face_encodings = face_recognition.face_encodings(image, face_locations)
    
            for encoding in face_encodings:
                names.append(name)
                encodings.append(encoding)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            continue
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)




def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], unknown_encoding)
    votes = Counter(name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def recognize_faces(image_location: str,model: str = "hog",encodings_location: Path = DEFAULT_ENCODINGS_PATH,) -> None:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(input_image, input_face_locations)
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        print(name, bounding_box)


def recognize_facesFromCameraStream(imgArray:np.array,model: str = "hog",encodings_location: Path = DEFAULT_ENCODINGS_PATH,) -> None:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)


    input_face_locations = face_recognition.face_locations(imgArray, model=model)
    input_face_encodings = face_recognition.face_encodings(imgArray, input_face_locations)
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        return (name, bounding_box)





# encode_known_faces()

camera = cv2.VideoCapture(0)

def closeHandling():
    print("House cleaning...")
    camera.release()
    cv2.destroyAllWindows()

atexit.register(closeHandling)

while True:
    success, img = camera.read()
    if success:
        imgs = np.array(img)
        try:
            name, boundingBoxPoints = recognize_facesFromCameraStream(img)
            img = cv2.putText(img, name, (boundingBoxPoints[3], boundingBoxPoints[0]), cv2.FONT_HERSHEY_COMPLEX,  fontScale, color, thickness, cv2.LINE_AA) 
            img = cv2.rectangle(img, (boundingBoxPoints[3], boundingBoxPoints[0]), (boundingBoxPoints[1], boundingBoxPoints[2]), (255, 0,0), 2)
            # print(boundingBoxPoints)

        except Exception as e:
            continue

        cv2.imshow("capture", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

       
        


