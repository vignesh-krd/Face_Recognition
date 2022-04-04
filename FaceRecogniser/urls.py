from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
]
