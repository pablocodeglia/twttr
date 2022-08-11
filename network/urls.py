
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following_view, name="following"),
    path("new", views.new_post_view, name="new"),
    path("edit/<int:id>", views.edit_post_view, name="edit"),
    path("profile/<int:id>", views.profile_view, name="profile"),
    path("like/<int:post_id>", views.like, name="like"),
    path("follow/<int:id>", views.follow_user, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
