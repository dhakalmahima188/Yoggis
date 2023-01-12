from django.urls import path
from . import views

urlpatterns = [
    path('yoga/',views.yoga,name='yoga'),
    path('video_feed/',views.videofeed,name='video_feed'),
    path('',views.home,name='home'),
    path('general',views.general,name='general'),
    path('squad/',views.squad,name='squad'),
    path('squad/session/',views.session,name='session'),


]