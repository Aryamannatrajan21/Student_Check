# student_discussion/urls.py
from django.conf.urls.static import static
from django.urls import path

from studentcheck import settings
from . import views

urlpatterns = [
    path('', views.discussion_home, name='discussion_home'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),
    path('chatroom/<int:chatroom_id>/', views.chatroom, name='chatroom'),
    path('chatroom/<int:chatroom_id>/send_message/', views.send_message, name='send_message'),
    path('give_feedback/', views.give_feedback, name='give_feedback'),
    path('join_chatroom/', views.join_chatroom, name='join_chatroom'),
    path('give-feedback/', views.give_feedback, name='give_feedback'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
