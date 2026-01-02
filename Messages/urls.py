from django.urls import path
from . import views

urlpatterns = [
    path("", views.messages_home, name="messages_home"),
    path("chat/<int:user_id>/", views.chat_view, name="chat"),
    path("chat/<int:user_id>/delete/", views.delete_chat, name="delete_chat"),
    path("chat/<int:user_id>/block/", views.block_user, name="block_user"),
    path("chat/<int:user_id>/unblock/", views.unblock_user, name="unblock_user"),


]
