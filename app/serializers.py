from rest_framework import serializers
from .models import Posts
from .models import Human, HumanStatistics


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class HumanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Human
        fields = '__all__'


class HumanStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanStatistics
        fields = '__all__'

