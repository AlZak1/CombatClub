from django.contrib import admin
from .models import Human, HumanStatistics

# Register your models here.

admin.site.register(Human)
admin.site.register(HumanStatistics)
