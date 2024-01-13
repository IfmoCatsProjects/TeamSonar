from django.urls import path
from . import views

urlpatterns = [
    path('message', views.message, name='message'),
    path('message_delete', views.message_delete, name='message_delete'),
    path('chats', views.ChatsView.as_view(), name='chats'),
    path('chat', views.ChatRoomView.as_view(), name='chat')
]