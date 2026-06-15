from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_room, name='chat'),
    path('<int:recipient_id>/', views.chat_room, name='chat_with_user'),
    path('send/', views.send_message, name='send_message'),
]

