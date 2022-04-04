import cv2
import os
import numpy as np
import face_recognition

faceNames = []
images = []


class Live_Face_Recogniser:
    def __init__(self):
        if not faceNames:
            # For Input Faces
            # path = '..\Images'
            path = os.path.abspath('Images')
            print("Absolute Path", path)
            myList = os.listdir(path)
            print("My List", myList)

            for cl in myList:
                curImg = cv2.imread(f'{path}/{cl}')
                images.append(curImg)
                faceNames.append(os.path.splitext(cl)[0])
            print("Face Names: ", faceNames)

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
        encodeListKnown = []
        if not encodeListKnown:
            encodeListKnown = Live_Face_Recogniser.findEncodings(images)
            print("Called Face Encodings")

        imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

        # It Returns Top(y1), Right(x2), Bottom(y2), left(x1)
        faceCurFrame = face_recognition.face_locations(imgSmall)
        encodeCurFrame = face_recognition.face_encodings(
            imgSmall, faceCurFrame)

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(
                encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(
                encodeListKnown, encodeFace)
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
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    # cv2.rectangle(img, (x1, y1 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6,),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    print("Rectangle Drawn on the face")
            except Exception as e:
                print(e)
                pass
        return img
        # cv2.imshow("WebCam", img)
        # cv2.waitKey(1)
