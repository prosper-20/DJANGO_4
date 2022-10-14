import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from blog.models import Post
from .serializers import PostSerializer, UserRegistrationSerializer, UserPropertiesSerializer
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from blog.api import serializers

class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@api_view(["GET", "POST"])
def api_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        user = request.user
        post = Post(author=user)

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def api_detail_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def api_update_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user != post.author:
        return Response({"Error": "You cannot update another user's post"})

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def api_delete_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user != post.author:
        return Response({"Error": "You cannot delete another user's post"})

    if request.method == "DELETE":
        operation = post.delete()
        data = {}
        if operation:
            data["Success"] = "Post deleted sucessfully!"
        else:
            data["Failure"] = "Post deletion failed"
        return Response(data=data)


@api_view(["POST"])
def api_create_user(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = {}
            user = serializer.save()
            data["Success"] = "User creation successful!"
            data["username"] = user.username
            data["email"] = user.email
            token = Token.objects.create(user=user).key
            data["token"] = token
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["title", "content", "slug", "author__username"]


# class UserPropertiesView(RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.get(username=user.username)
#     lookup_field = us
#     serializer_class = UserPropertiesSerializer
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPropertiesSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserPropertiesSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_user_properties(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserPropertiesSerializer(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["PUT"])
@permission_classes((IsAuthenticated,))
def update_user_properties(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = UserPropertiesSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data["Success"] = "Account updated successfully"
            data["username"] = user.username
            data["email"] = user.email
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserList2(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPropertiesSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPropertiesSerializer







    