# Accounts/urls.py
from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    edit_profile,
    delete_account,
    user_profile,
    search_user,
)

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # profile (logged-in user)
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("delete-account/", delete_account, name="delete_account"),

    # public user profile
    path("profile/<str:username>/", user_profile, name="user_profile"),
    path("search/", search_user, name="search_user"),

]
