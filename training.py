import face_recognition
import os
import pickle


dataset_path = "datasets/"

known_encodings = []
known_names = []

def EncodingNamesDirs():
    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)

        if not os.path.isdir(person_folder):
            continue

        for image_name in os.listdir(person_folder):
            image_path = os.path.join(person_folder, image_name)

            image = face_recognition.load_image_file(image_path)

            encodings = face_recognition.face_encodings(image)

            for encoding in encodings:
                known_encodings.append(encoding)
                known_names.append(person_name)

    try:
        with open('encodings.pkl', 'wb') as f:
            pickle.dump((known_encodings, known_names), f)
            return True
    except Exception as e:
        print("=>  Failed to save training into picke file")
        return False
    


print(EncodingNamesDirs())