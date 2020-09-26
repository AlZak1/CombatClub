from time import timezone

from rest_framework.permissions import IsAuthenticated

from .services import HumanService

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Human, HumanStatistics
from .serializers import HumanSerializer, HumanStatisticsSerializer
import datetime

# Create your views here.


class HumanView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer, HumanStatisticsSerializer
    queryset = Human.objects.all()
    human_service = HumanService([])

    def post(self, request, *args, **kwargs):
        username = request.user.id
        human = request.data
        human["user"] = username
        human_statistics = request.data
        human_statistics['user'] = username
        serializer = HumanStatisticsSerializer(data=human_statistics)
        if serializer.is_valid():
            # serializer.save()
            pass
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


class HumanStatisticsView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HumanStatisticsSerializer
    queryset = HumanStatistics.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = HumanStatisticsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data_to_filter = request.data
        if data_to_filter['isAttack'] == 'all' and data_to_filter['fromDate'] is None and data_to_filter['toDate'] is None:
            queryset = HumanStatistics.objects.all()
        elif data_to_filter['isAttack'] == 'defense' and data_to_filter['fromDate'] is None and data_to_filter['toDate'] is None:
            queryset = HumanStatistics.objects.filter(isAttack=False)
        elif data_to_filter['isAttack'] == 'attack' and data_to_filter['fromDate'] is None and data_to_filter['toDate'] is None:
            queryset = HumanStatistics.objects.filter(isAttack=True)
        elif data_to_filter['isAttack'] is None and data_to_filter['fromDate'] is not None and data_to_filter['toDate'] is not None:
            queryset = HumanStatistics.objects.filter(date_without_time__range=(data_to_filter['fromDate'], data_to_filter['toDate']))
        elif data_to_filter['isAttack'] == 'attack' and data_to_filter['fromDate'] is not None and data_to_filter['toDate'] is not None:
            queryset = HumanStatistics.objects.filter(isAttack=True, date_without_time__range=(data_to_filter['fromDate'], data_to_filter['toDate']))
        elif data_to_filter['isAttack'] == 'defense' and data_to_filter['fromDate'] is not None and data_to_filter['toDate'] is not None:
            queryset = HumanStatistics.objects.filter(isAttack=False, date_without_time__range=(data_to_filter['fromDate'], data_to_filter['toDate']))
        elif data_to_filter['isAttack'] == 'all' and data_to_filter['fromDate'] is not None and data_to_filter['toDate'] is not None:
            queryset = HumanStatistics.objects.filter(date_without_time__range=(data_to_filter['fromDate'], data_to_filter['toDate']))
        serializer = HumanStatisticsSerializer(queryset, many=True)

        return Response(serializer.data)


class LoadPageView(APIView):
    serializer_class = HumanSerializer

    def get(self, request):
        username = request.user.id
        human_1 = Human.objects.get(user=1)
        human_2 = Human.objects.get(user=2)
        human_object = {'user': username, 'total_damage': None, 'enemy_damage': None}
        if username == 1:
            human_object['total_damage'] = human_1.total_damage
            human_object['enemy_damage'] = human_1.enemy_damage
        else:
            human_object['total_damage'] = human_2.total_damage
            human_object['enemy_damage'] = human_2.enemy_damage
        serializer = HumanSerializer(data=human_object)
        if serializer.is_valid():
            pass
        return Response(serializer.data)
