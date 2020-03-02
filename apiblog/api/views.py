from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
import clearbit
from django.http import JsonResponse
import requests
import json


from .models import Posts, Likes
from django.contrib.auth.models import User
from .serializers import PostsSerializer, LikesSerializer, UserSerializer, LoginSerializer


class PostsList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

    def get_queryset(self):
        qs = self.queryset.filter(created_by=self.request.user)
        return qs


class LikesList(generics.ListCreateAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


def clearbit_emails(request):
    clearbit.key = 'sk_262741b24a40538c369d3a89550ad140'
    users = User.objects.all()
    emails = users.values("email")
    res_list = []
    for email in emails:
        try:
            lookup = clearbit.Enrichment.find(email=email, stream=True)
            name = str(lookup['person']["name"]["givenName"])
            surname = str(lookup['person']["name"]["familyName"])
            res = [name, surname]
        except:
            res = ["n/a", "n/a"]
        res_list.append(res)
        data = {"Enrichment results": res_list}
    return JsonResponse(data)

