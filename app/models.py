from django.db import models
from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Posts(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


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
