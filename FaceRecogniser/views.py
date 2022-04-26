from django import views
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import threading
from FaceRecogniser.Live_Face_Recog import Live_Face_Recogniser
from tkinter import filedialog

# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def live_recognition(request):
    return render(request, "Live_Recognition.html")


def single_face(request):
    return render(request, "SingleFace.html")


def multi_face(request):
    return render(request, "MultiFace.html")


def pre_recorded(request):
    return render(request, "Pre_Recorded.html")


def single_file(request):
    return render(request, "Singlefile.html")


def multi_file(request):
    return render(request, "Multifile.html")


def facecam_feed(request):
    Cam = VideoCamera()
    response = StreamingHttpResponse(
        gen(Cam), content_type="multipart/x-mixed-replace; boundary=frame")
    return response
# to capture video class


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.success, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        lfr_object = Live_Face_Recogniser()
        image = lfr_object.compare_faces(image)
        _, jpeg = cv2.imencode(".jpg", image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.success, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
