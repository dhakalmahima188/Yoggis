from django.urls import path
from . import views

urlpatterns = [
    path('yoga/', views.yoga, name='yoga'),
    path('video_feed/', views.videofeed, name='video_feed'),
    path('', views.home, name='home'),
    path('general', views.general, name='general'),
    path('squad/', views.squad, name='squad'),
    path('squad/session/', views.session, name='session'),
    path('general/', views.general, name='general'),
    path('chronic/', views.chronic, name='chronic'),
    path('tpose/', views.tpose, name='tpose'),
    path('general', views.general, name='general'),
    path('yoga/<int:pk1>', views.yoga_detail_view, name='yoga-detail'),
    # path('challenges/',views.challenges,name='challenges'),
    # path('leaderboard/',views.leaderboard,name='leaderboard'),

]
