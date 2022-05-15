import imp
from importlib.resources import path
from django import views
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import cv2
import threading
from FaceRecogniser import Live_Face_Recog
from FaceRecogniser.Live_Face_Recog import Live_Face_Recogniser
from tkinter import filedialog

from FaceRecogniser.Live_Face_Recog import Rec_Face_Recogniser


# Create your views here.
is_single = True
is_file = False


# def home(request):
#     response = "Hiiiiiii"
#     return StreamingHttpResponse(response, content_type="text/plain")


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def live_recognition(request):
    return render(request, "Live_Recognition.html")


def single_face(request):
    global is_single, is_file
    is_single = True
    is_file = False
    return render(request, "SingleFace.html", {'path': False})


def multi_face(request):
    global is_single, is_file
    is_single = False
    is_file = False
    return render(request, "MultiFace.html", {'path': False})


def pre_recorded(request):
    return render(request, "Pre_Recorded.html")


def single_file(request):
    global is_single, is_file
    is_single = True
    is_file = True
    return render(request, "Singlefile.html", {'path': False, 'video_path': False})


def multi_file(request):
    global is_single, is_file
    is_single = False
    is_file = True
    return render(request, "Multifile.html", {'path': False, 'video_path': False})


def facecam_feed(request):
    Cam = VideoCamera()
    if not is_file:
        response = StreamingHttpResponse(
            gen(Cam), content_type="multipart/x-mixed-replace; boundary=frame")
        return response
    return None


def rec_feed(request):
    if is_file:
        rfr_object = Rec_Face_Recogniser(is_single)
        face_details_list = rfr_object.compare_faces(
            Live_Face_Recog.video_path)
        print(face_details_list)
        # time_details = ""
        # for detail in face_details_list:
        #     time_details += (f"{detail}\n")
        # print(time_details)
    if is_single:
        return render(request, "SingleFile.html", {'path': True, 'video_path': True, 'face_details_list': face_details_list})
    else:
        return render(request, "MultiFile.html", {'path': True, 'video_path': True, 'face_details_list': face_details_list})

# to capture video class


class VideoCamera(object):
    def __init__(self):
        if is_file:
            # print("Video Path: ", Live_Face_Recog.video_path)
            # self.video = cv2.VideoCapture(Live_Face_Recog.video_path)
            rfr_object = Rec_Face_Recogniser(is_single)
            face_details_list = rfr_object.compare_faces(
                Live_Face_Recog.video_path)
            print(face_details_list)
        else:
            self.video = cv2.VideoCapture(0)
            (self.success, self.frame) = self.video.read()
            threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        while True:
            image = self.frame
            lfr_object = Live_Face_Recogniser(is_single)
            image = lfr_object.compare_faces(image)
            _, jpeg = cv2.imencode(".jpg", image)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
            return jpeg.tobytes()

    def update(self):
        while True:
            (self.success, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
