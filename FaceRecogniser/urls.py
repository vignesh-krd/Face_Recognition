from django.urls import path

from FaceRecogniser import Live_Face_Recog
from . import views

urlpatterns = [
    path('', views.index, name="index"),
#     path('home', views.home, name="home"),
    path('index', views.index, name="index"),
    path('about', views.about, name="about"),
    path('live_recognition', views.live_recognition, name="live_recognition"),
    path('single_face', views.single_face, name="single_face"),
    path('multi_face', views.multi_face, name="multi_face"),
    path('pre_recorded', views.pre_recorded, name="pre_recorded"),
    path('single_file', views.single_file, name="single_file"),
    path('multi_file', views.multi_file, name="multi_file"),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    path('rec_feed', views.rec_feed, name='rec_feed'),
    path('live_open_file', Live_Face_Recog.live_open_file, name="live_open_file"),
    path('live_open_directory', Live_Face_Recog.live_open_directory,
         name="live_open_directory"),
    path('rec_open_file', Live_Face_Recog.rec_open_file, name="rec_open_file"),
    path('rec_open_directory', Live_Face_Recog.rec_open_directory,
         name="rec_open_directory"),
    path('file_open_video', Live_Face_Recog.file_open_video, name="file_open_video"),
    path('dir_open_video', Live_Face_Recog.dir_open_video, name="dir_open_video"),
]
