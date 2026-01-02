# Connections/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("requests/", views.incoming_requests, name="incoming_requests"),
    path("network/", views.my_network, name="my_network"),

    path("ajax/connect/", views.send_connection_request, name="connect"),
    path("ajax/respond/", views.respond_request_ajax, name="respond_request_ajax"),
    path("ajax/follow/", views.follow_user, name="follow"),
    path("ajax/unfollow/", views.unfollow_user, name="unfollow"),
    path("ajax/disconnect/", views.disconnect_user, name="disconnect"),

    path("connections/", views.connections_list, name="connections_list"),
    path("followers/", views.followers_list, name="followers"),
]
