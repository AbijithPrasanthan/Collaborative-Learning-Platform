from django.urls import path
from django.conf.urls import include
from CLP import views


path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-detail'),
path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),

urlpatterns = [
    path('cam', views.cam, name='cam'),
    path('mask_feed', views.mask_feed, name='mask_feed'),
    path('login/', views.register, name='login'),
    path('home/', views.index, name='home'),
    path('login/', views.user_logout, name='user_logout'),
    path('new/', views.newMeeting, name='new_meeting'),
    path('meeting/<str:id>/', views.meeting, name='meeting'),
    path('chat/', views.chat, name='chat'),
    path('send/', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('chat/checkview/<str:room>/', views.room, name='room'),
    path('chat/checkview/', views.checkview, name='checkview'),
    path('home/<int:id>/show',  views.showDetails, name='showdetails'),
    path('notes/', views.notes, name='notes'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-detail'),
    path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-detail'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),
    path('homework/', views.homework, name='homework'),
    path('relax/', views.relax, name='relax'),
    path('bubbleshooter/', views.bubbleshooter, name='bubbleshooter'),
    path('wordle/', views.wordle, name='wordle')
]
