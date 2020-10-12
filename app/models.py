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
    isAttack = models.BooleanField(default=False, null=True, blank=True)
    total_damage = models.IntegerField(default=False)
    enemy_damage = models.IntegerField(default=False)
    current_damage = models.IntegerField(default=False)
    current_enemy_damage = models.IntegerField(default=False)
    roomId = models.IntegerField(default=None, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    date_without_time = models.DateField(null=True, blank=True)


class Room(models.Model):
    player_one = models.IntegerField(null=True, blank=True)
    player_two = models.IntegerField(null=True, blank=True)


