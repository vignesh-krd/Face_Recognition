from importlib.resources import path
import tkinter
import cv2
import os
from django.shortcuts import render
import numpy as np
import face_recognition
from tkinter import filedialog, Tk

is_single1 = True

faceNames = []
images = []
encodeListKnown = []
frame_count = 0

path = ""
video_path = ""


class Live_Face_Recogniser:
    def __init__(self, is_single):
        global path, is_single1
        is_single1 = is_single
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
        imgSmall = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
        imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
                    # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (172, 189, 46), 2)
                    cv2.putText(img, name, (x1 + 6, y2 - 6,),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    print("Rectangle Drawn on the face")
            except Exception as e:
                print(e)
                pass
        return img
        # cv2.imshow("WebCam", img)
        # cv2.waitKey(1)


class Rec_Face_Recogniser:
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
                    Rec_Face_Recogniser.findEncodings(images))
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
                    Rec_Face_Recogniser.findEncodings(images))
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

    def compare_faces(self, video_path):
        video = cv2.VideoCapture(video_path)
        face_details_list = []
        while True:
            (success, img) = video.read()
            if success:
                imgSmall = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
                imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
                            time_stamp = str(
                                round(video.get(cv2.CAP_PROP_POS_MSEC)/1000, 2))
                            time_details = (
                                f"Name:'{name}' Timestamp is: '{time_stamp}'\n")
                            # face_details += face_details+"\n"
                            face_details_list.append(time_details)
                            print(time_details)
                            y1, x2, y2, x1 = faceLoc
                            # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                            img = cv2.rectangle(
                                img, (x1, y1), (x2, y2), (172, 189, 46), 2)
                            # cv2.rectangle(img, (x1, y1 - 35), (x2, y2), (255, 0, 255), cv2.FILLED)
                            img = cv2.putText(img, name, (x1 + 6, y2 - 6,),
                                              cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                            print("Rectangle Drawn on the face")
                    except Exception as e:
                        print(e)
                        pass
            else:
                break
        face_detail = ""
        face_detail = face_detail.join(face_details_list)
        return face_detail
        # return img
        # cv2.imshow("WebCam", img)
        # cv2.waitKey(1)


def live_open_file(request):
    global path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Choose the photo of the Person to find")
    print(path)
    return render(request, "SingleFace.html", {'path': True})


def live_open_directory(request):
    global path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    path = filedialog.askdirectory(
        title="Choose the folder that contains photos of the Persons to find")
    print(path)
    return render(request, "MultiFace.html", {'path': True})


def rec_open_file(request):
    global path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Choose the photo of the Person to find")
    print(path)
    if is_single1:
        file = "SingleFile.html"
    else:
        file = "MultiFile.html"
    if len(video_path) == 0:
        return render(request, file, {'path': True, 'video_path': False})
    else:
        return render(request, file, {'path': True, 'video_path': True})


def rec_open_directory(request):
    global path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    path = filedialog.askdirectory(
        title="Choose the folder that contains photos of the Persons to find")
    print(path)
    # if is_single1:
    #     file = "SingleFile.html"
    # else:
    #     file = "MultiFile.html"
    if len(video_path) == 0:
        return render(request, "MultiFile.html", {'path': True, 'video_path': False})
    else:
        return render(request, "MultiFile.html", {'path': True, 'video_path': True})


def file_open_video(request):
    global video_path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    video_path = filedialog.askopenfilename(title="Choose the video to scan")
    print(video_path)
    if is_single1:
        file = "SingleFile.html"
    else:
        file = "MultiFile.html"
    if len(path) == 0:
        return render(request, file, {'path': False, 'video_path': True})
    else:
        return render(request, file, {'path': True, 'video_path': True})


def dir_open_video(request):
    global video_path
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    video_path = filedialog.askopenfilename(title="Choose the video to scan")
    print(video_path)
    # if is_single1:
    #     file = "SingleFile.html"
    # else:
    #     file = "MultiFile.html"
    if len(path) == 0:
        return render(request, "MultiFile.html", {'path': False, 'video_path': False})
    else:
        return render(request, "MultiFile.html", {'path': True, 'video_path': True})
