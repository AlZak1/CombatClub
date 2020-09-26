from rest_framework import serializers
from .models import Human, HumanStatistics


class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = '__all__'


class HumanStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanStatistics
        fields = '__all__'

