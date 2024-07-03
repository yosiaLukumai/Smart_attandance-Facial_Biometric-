import face_recognition
import os
import pickle
import cv2
import os

name = 'Alesha'
SessionImageEnded = False
OutputDir = "datasets"+"/"+ name
dataset_path = "datasets/"

known_encodings = []
known_names = []

cam = cv2.VideoCapture(0)
cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 320, 240)
img_counter = 0

if not os.path.exists(OutputDir):
    os.makedirs(OutputDir)

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
    





def TakePics():
    print("--------------------------")
    global img_counter

    global SessionImageEnded
    print("Local ", img_counter, SessionImageEnded)
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error:  failed to grab frame")
            SessionImageEnded = True
            break
        cv2.imshow("press space to take a photo", frame)

        k = cv2.waitKey(1)
        if k%256 == 27 or k == ord('q'):
            # ESC pressed
            print("Closing the, closing...")
            SessionImageEnded = True
            break
        elif k%256 == 32:
            fullPath = os.path.join(OutputDir, name+str(img_counter)+".jpg")
            try:
                written = cv2.imwrite(fullPath, frame)
            except Exception as e:
                print("Error: ", e)
            img_counter += 1




def PerfomJucntions():
    # preparing of the training
    if SessionImageEnded:
        if img_counter >=  10:
            print("=========================TRAINING SESSION=====================")
            EncodingNamesDirs()
            print("======================= Wooh Training Ended ===================")

        else:
            print("ERROR:  TAKE MORE PICS AT LEAST 10")
    else: 
        print("ERROR: Take first Pics")





if __name__ == "__main__":
    try:
        TakePics()
        cam.release()
        cv2.destroyAllWindows()
        PerfomJucntions()
    except Exception as e:
        print("Error: ", e)