from django.urls import path
from . import views

urlpatterns = [
    path('yoga/',views.yoga,name='yoga'),
    path('video_feed/',views.videofeed,name='video_feed')
]