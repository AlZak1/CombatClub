from rest_framework import serializers
from .models import Human, Room


class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

