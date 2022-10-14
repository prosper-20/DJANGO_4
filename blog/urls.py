from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>/", views.detail, name="post-detail"),
    path("profile", views.profile, name="profile")
]