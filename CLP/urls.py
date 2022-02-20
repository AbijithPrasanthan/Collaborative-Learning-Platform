from django.urls import path
from django.conf.urls import include
from CLP import views


urlpatterns = [
    path('login/', views.register, name='login'),
    path('home/', views.index, name='home'),
    path('login/', views.user_logout, name='user_logout'),
    path('new/', views.newMeeting, name='new_meeting'),
    path('meeting/', views.meeting, name='meeting'),
    path('chat/', views.chat, name='chat'),
    path('send/', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('chat/checkview/<str:room>/', views.room, name='room'),
    path('chat/checkview/', views.checkview, name='checkview'),
    path('home/<int:id>/show',  views.showDetails, name='showdetails')
]
