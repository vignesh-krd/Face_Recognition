from django.urls import path

from FaceRecogniser import Live_Face_Recog
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('index', views.index, name="index"),
    path('about', views.about, name="about"),
    path('live_recognition', views.live_recognition, name="live_recognition"),
    path('single_face', views.single_face, name="single_face"),
    path('multi_face', views.multi_face, name="multi_face"),
    path('pre_recorded', views.pre_recorded, name="pre_recorded"),
    path('single_file', views.single_file, name="single_file"),
    path('multi_file', views.multi_file, name="multi_file"),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    path('open_file', Live_Face_Recog.open_file, name="open_file"),
    path('open_directory', Live_Face_Recog.open_directory, name="open_directory"),
]
