import cv2
import os

name = 'Yosia'
OutputDir = "datasets"+"/"+name

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 640, 480)

img_counter = 0


#if output dir doesn't exist force to create

if not os.path.exists(OutputDir):
    os.makedirs(OutputDir)
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        fullPath = os.path.join(OutputDir, name+str(img_counter)+".jpg")
        try:
            written = cv2.imwrite(fullPath, frame)
        except Exception as e:
            print(e)
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
