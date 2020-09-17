from .services import HumanService
import json
from collections import namedtuple
import jwt
from django.contrib.auth import user_logged_in
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Posts, Human, User
from .serializers import PostSerializer, HumanSerializer, UserSerializer


# Create your views here.


class PostView(RetrieveAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Posts.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class HumanView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer
    queryset = Human.objects.all()
    human_service = HumanService([])

    def post(self, request, *args, **kwargs):
        username = request.user.id
        a = request.data
        a["user"] = username
        serializer = HumanSerializer(data=a)
        if serializer.is_valid():
            human = serializer.data
            self.human_service.append_human_list(human)
            total_score = self.human_service.process_human_list()
            print(total_score)
        return Response(total_score)

    def play(self, request):
        pass


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
