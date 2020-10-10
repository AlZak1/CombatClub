from django.db import models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Human(models.Model):
    head = models.BooleanField(default=False)
    body = models.BooleanField(default=False)
    leftHand = models.BooleanField(default=False)
    rightHand = models.BooleanField(default=False)
    leftLeg = models.BooleanField(default=False)
    rightLeg = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    isAttack = models.BooleanField(default=False)
    total_damage = models.IntegerField(default=None)
    enemy_damage = models.IntegerField(default=None)
    current_damage = models.IntegerField(default=None)
    current_enemy_damage = models.IntegerField(default=None)


class HumanStatistics(models.Model):
    head = models.BooleanField(default=False)
    body = models.BooleanField(default=False)
    leftHand = models.BooleanField(default=False)
    rightHand = models.BooleanField(default=False)
    leftLeg = models.BooleanField(default=False)
    rightLeg = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    isAttack = models.BooleanField(default=False)
    date_without_time = models.DateField(auto_now_add=True)


class Room(models.Model):
    player_one = models.IntegerField(null=True)
    player_two = models.IntegerField(null=True)


