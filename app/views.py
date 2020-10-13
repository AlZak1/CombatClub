from .services import HumanService

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Human, Room
from .serializers import HumanSerializer, RoomsSerializer


# Create your views here.


class HumanView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer
    human_service = HumanService([], [])

    def post(self, request):
        player = player_turn_post(self, request)
        serializer = HumanSerializer(data=player)
        if serializer.is_valid():
            pass
        return Response(serializer.data)

    def get(self, request):
        human = player_turn_get(self, request)
        serializer = HumanSerializer(data=human)
        if serializer.is_valid():
            self.human_service.human_list.clear()
        return Response(serializer.data)


def player_turn_get(self, request):
    username = request.user.id
    data = request.headers
    room_id = data['Data']
    current_room = Room.objects.get(id=room_id)
    human = {'user': username, 'total_damage': None, 'enemy_damage': None, 'current_damage': None,
             'current_enemy_damage': None}
    total_score = self.human_service.process_human_list()
    human_1 = Human.objects.filter(user=current_room.player_one).latest('id')
    human_2 = Human.objects.filter(user=current_room.player_two).latest('id')
    if len(total_score) == 2:
        if username == current_room.player_one:
            human = player_one_turn(request, total_score, human_1)
        else:
            human = player_two_turn(request, total_score, human_2)
    print('Данные отсылаемые клиенту по GET:', human)
    return human


def player_turn_post(self, request):
    human_service = HumanService([], [])
    username = request.user.id
    human = request.data
    room_id = human['roomId']
    current_room = Room.objects.get(id=room_id)
    human["user"] = username
    human_statistics = request.data
    if username == current_room.player_one:
        human_statistics['user'] = current_room.player_one
    elif username == current_room.player_two:
        human_statistics['user'] = current_room.player_two
    serializer = HumanSerializer(data=human_statistics)
    if serializer.is_valid():
        pass
        # serializer.save()
    self.human_service.append_human_list(human)
    total_score = self.human_service.process_human_list()
    self.human_service.append_room_list(current_room)
    response_data = {'user': username, 'total_damage': None, 'enemy_damage': None, 'current_damage': None,
                     'current_enemy_damage': None}
    human_1 = Human.objects.filter(user=current_room.player_one).latest('id')
    human_2 = Human.objects.filter(user=current_room.player_two).latest('id')
    if len(total_score) == 2:
        if username == current_room.player_one:
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
    return response_data


def player_one_turn(request, total_score, human_1):
    username = request.user.id
    response_data = {'user': username, 'total_damage': total_score['damage1'] + human_1.total_damage,
                     'enemy_damage': total_score['damage2'] + human_1.enemy_damage,
                     'current_damage': total_score['damage1'], 'current_enemy_damage': total_score['damage2']}

    human_1.total_damage = response_data['total_damage']
    human_1.save()
    human_1.enemy_damage = response_data['enemy_damage']
    human_1.save()
    return response_data


def player_two_turn(request, total_score, human_2):
    username = request.user.id
    response_data = {'user': username, 'total_damage': total_score['damage2'] + human_2.total_damage,
                     'enemy_damage': total_score['damage1'] + human_2.enemy_damage,
                     'current_damage': total_score['damage2'], 'current_enemy_damage': total_score['damage1']}

    human_2.total_damage = response_data['total_damage']
    human_2.save()
    human_2.enemy_damage = response_data['enemy_damage']
    human_2.save()
    return response_data


class HumanStatisticsView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = HumanSerializer
    queryset = Human.objects.all()

    def get(self, request, *args, **kwargs):
        params = request.GET
        queryset = self.get_queryset()
        print('params', params)
        if params is None:
            queryset = self.get_queryset()
        elif params is not None:
            attack = request.GET.get('isAttack')
            fromDate = request.GET.get('fromDate')
            toDate = request.GET.get('toDate')
            if attack == 'all' and fromDate is None and toDate is None:
                queryset = Human.objects.all()
            elif attack == 'defense' and fromDate is None and toDate is None:
                queryset = Human.objects.filter(isAttack=False)
            elif attack == 'attack' and fromDate is None and toDate is None:
                queryset = Human.objects.filter(isAttack=True)
            elif attack is None and fromDate is not None and toDate is not None:
                queryset = Human.objects.filter(date_without_time__range=(fromDate, toDate))
            elif attack == 'attack' and fromDate is not None and toDate is not None:
                queryset = Human.objects.filter(isAttack=True, date_without_time__range=(fromDate, toDate))
            elif attack == 'defense' and fromDate is not None and toDate is not None:
                queryset = Human.objects.filter(isAttack=False, date_without_time__range=(fromDate, toDate))
            elif attack == 'all' and fromDate is not None and toDate is not None:
                queryset = Human.objects.filter(date_without_time__range=(fromDate, toDate))
        serializer = HumanSerializer(queryset, many=True)
        return Response(serializer.data)


class LoadPageView(APIView):
    serializer_class = HumanSerializer

    def get(self, request):
        username = request.user.id
        data = request.headers
        room_id = data['Data']
        current_room = Room.objects.get(id=room_id)
        human_1 = Human.objects.filter(user=current_room.player_one).latest('id')
        human_2 = Human.objects.filter(user=current_room.player_two).latest('id')
        human_object = {'user': username, 'total_damage': None, 'enemy_damage': None}
        if username == current_room.player_one:
            human_object['total_damage'] = human_1.total_damage
            human_object['enemy_damage'] = human_1.enemy_damage
        else:
            human_object['total_damage'] = human_2.total_damage
            human_object['enemy_damage'] = human_2.enemy_damage
        print('human object', human_object)
        serializer = HumanSerializer(data=human_object)
        if serializer.is_valid():
            pass
        return Response(serializer.data)


class RoomsView(APIView):
    serializer_class = HumanSerializer

    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        room = Room.objects.all()
        return room

    def get(self, request):
        queryset = self.get_queryset()
        serializer = RoomsSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        username = request.user.id
        print('dssa', username)
        user = {'user': username}
        data = request.data
        print('data', data)
        data_id = data['id']
        room = Room.objects.get(id=data_id)
        if room.user_1 is None:
            print('sasdf', user['user'])
            print(username)
            room.user_1 = request.user
            room.save()
        elif room.user_2 is None:
            room.user_2 = request.user
            room.save()
        else:
            print('комната занята')
        serializer = RoomsSerializer(data=room)
        if serializer.is_valid():
            pass

        return Response(serializer.data)
