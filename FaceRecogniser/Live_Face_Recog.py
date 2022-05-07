from importlib.resources import path
import cv2
import os
from django.shortcuts import render
import numpy as np
import face_recognition
from tkinter import filedialog

faceNames = []
images = []
encodeListKnown = []

path = ""


class Live_Face_Recogniser:
    def __init__(self, is_single):
        global path
        if not faceNames:
            # For Input Faces
            # path = '..\Images'
            # path = os.path.abspath('Images')
            if is_single:
                # path = filedialog.askopenfilename()
                print("Absolute Path:", path)
                img = cv2.imread(path)
                images.append(img)
                file_name = path.split('/')[-1]
                faceNames.append(file_name.split('.')[0])
                print("Face Names: ", faceNames)
                encodeListKnown.append(
                    Live_Face_Recogniser.findEncodings(images))
                print("Called Face Encodings")
            else:
                # path = filedialog.askdirectory()
                print("Absolute Path", path)
                myList = os.listdir(path)
                print("My List", myList)

                for name in myList:
                    curImg = cv2.imread(f'{path}/{name}')
                    images.append(curImg)
                    faceNames.append(os.path.splitext(name)[0])
                print("Face Names: ", faceNames)
                encodeListKnown.append(
                    Live_Face_Recogniser.findEncodings(images))
                print("Called Face Encodings")
                # print("Encode list known:", encodeListKnown[0])

    def findEncodings(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        print("Encoding of known faces completed")
        return encodelist

# print(len(encodeListKnown))

# For Capturing Live Videos

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    def compare_faces(self, img):
        imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

        # It Returns Top(y1), Right(x2), Bottom(y2), left(x1)
        faceCurFrame = face_recognition.face_locations(imgSmall)
        encodeCurFrame = face_recognition.face_encodings(
            imgSmall, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown[0], encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown[0], encodeFace)
            # print("Face Distance: ", faceDis)
            matchIndex = 0
            # print("Match Faces", matches)
            try:
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = faceNames[matchIndex].upper()
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    img = cv2.rectangle(
                        img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    # cv2.rectangle(img, (x1, y1 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
                    img = cv2.putText(img, name, (x1 + 6, y2 - 6,),
                                      cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    print("Rectangle Drawn on the face")
            except Exception as e:
                print(e)
                pass
        return img
        # cv2.imshow("WebCam", img)
        # cv2.waitKey(1)


def open_file(request):
    global path
    path = filedialog.askopenfilename()
    print(path)
    return render(request, "SingleFace.html", {'path': True})


def open_directory(request):
    global path
    path = filedialog.askdirectory()
    print(path)
    return render(request, "MultiFace.html", {'path': True})

