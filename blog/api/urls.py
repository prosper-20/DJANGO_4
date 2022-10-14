from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.generics import ListCreateAPIView
from .serializers import UserPropertiesSerializer
from django.contrib.auth.models import User


urlpatterns = [
    path("home/", views.api_list_view, name="home2"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path("user/properties", views.get_user_properties, name="user-properties"),
    path("user/properties/update", views.update_user_properties, name="user-properties-update"),
    path("<slug:slug>/", views.api_detail_view, name="detail2"),
    path("<slug:slug>/update", views.api_update_view, name="update"),
    path("<slug:slug>/delete", views.api_delete_view, name="delete"),
    path("register", views.api_create_user, name="register"),
    path("login", obtain_auth_token, name="login"),
    path("list", views.PostListView.as_view(), name="list2"),

    
]