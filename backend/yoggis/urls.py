from django.urls import path
from . import views

urlpatterns = [
    path('yoga/', views.yoga, name='yoga'),
    path('video_feed/<int:pk>', views.videofeed, name='video_feed'),
    path('', views.home, name='home'),
    path('general', views.general, name='general'),
    path('squad/', views.squad, name='squad'),
    path('squad/session/', views.session, name='session'),
    path('general/', views.general, name='general'),
    path('chronic/', views.chronic, name='chronic'),
    path('backpain/', views.backpain, name='backpain'),
    path('<int:pk>', views.tpose, name='tpose'),
    path('general', views.general, name='general'),
    path('meditation/', views.meditation, name='meditation'),
    path('yoga/<int:pk1>', views.yoga_detail_view, name='yoga-detail'),
    path('user/updatesd/<int:pid>', views.updateUserDisorder, name='update-usersd'),
    # path('challenges/',views.challenges,name='challenges'),
    # path('leaderboard/',views.leaderboard,name='leaderboard'),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout",views.logout,name="logout"),
    path("profile",views.profile,name="profile"),
    path("congratulations",views.congratulations,name="congratulations"),

]
