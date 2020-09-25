from .services import HumanService
import json
from collections import namedtuple
import jwt
from django.contrib.auth import user_logged_in
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
    # permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer
    queryset = Human.objects.all()
    human_service = HumanService([])

    def post(self, request, *args, **kwargs):
        username = request.user.id
        human = request.data
        human["user"] = username
        self.human_service.append_human_list(human)
        total_score = self.human_service.process_human_list()
        print('total_score', total_score)
        response_data = {'user': username, 'total_damage': None, 'enemy_damage': None, 'current_damage': None, 'current_enemy_damage': None}
        human_1 = Human.objects.get(user=1)
        human_2 = Human.objects.get(user=2)
        if len(total_score) == 2:
            if username == 1:
                response_data['total_damage'] = total_score['damage1'] + human_1.total_damage
                response_data['enemy_damage'] = total_score['damage2'] + human_1.enemy_damage
                response_data['current_damage'] = total_score['damage1']
                response_data['current_enemy_damage'] = total_score['damage2']
                human_1.total_damage = response_data['total_damage']
                human_1.save()
                human_1.enemy_damage = response_data['enemy_damage']
                human_1.save()
            else:
                response_data['total_damage'] = total_score['damage2'] + human_2.total_damage
                response_data['enemy_damage'] = total_score['damage1'] + human_2.enemy_damage
                response_data['current_damage'] = total_score['damage2']
                response_data['current_enemy_damage'] = total_score['damage1']
                human_2.total_damage = response_data['total_damage']
                human_2.save()
                human_2.enemy_damage = response_data['enemy_damage']
                human_2.save()
        print('Данные отсылаемые клиенту по POST:', response_data)
        serializer = HumanSerializer(data=response_data)
        if serializer.is_valid():
            print('serializer', serializer.data)
            pass
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):

        username = request.user.id
        human = {'user': username, 'total_damage': None, 'enemy_damage': None, 'current_damage': None, 'current_enemy_damage': None}
        total_score = self.human_service.process_human_list()
        human_1 = Human.objects.get(user=1)
        human_2 = Human.objects.get(user=2)
        if len(total_score) == 2:
            if username == 1:
                human['total_damage'] = total_score['damage1'] + human_1.total_damage
                human['enemy_damage'] = total_score['damage2'] + human_1.enemy_damage
                human['current_damage'] = total_score['damage1']
                human['current_enemy_damage'] = total_score['damage2']
                human_1.total_damage = human['total_damage']
                human_1.save()
                human_1.enemy_damage = human['enemy_damage']
                human_1.save()
            else:
                human['total_damage'] = total_score['damage2'] + human_2.total_damage
                human['enemy_damage'] = total_score['damage1'] + human_2.enemy_damage
                human['current_damage'] = total_score['damage2']
                human['current_enemy_damage'] = total_score['damage1']
                human_2.total_damage = human['total_damage']
                human_2.save()
                human_2.enemy_damage = human['enemy_damage']
                human_2.save()
        print('edfsd', total_score)

        print('Данные отсылаемые клиенту по GET:', human)
        serializer = HumanSerializer(data=human)
        if serializer.is_valid():
            print('serializer', serializer.data)
            self.human_service.human_list.clear()
            pass
        return Response(human)

    def play(self, request):
        pass


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
