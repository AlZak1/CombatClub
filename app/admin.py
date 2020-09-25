from django.contrib import admin
from .models import Posts, Human, HumanStatistics

# Register your models here.

admin.site.register(Posts)
admin.site.register(Human)
admin.site.register(HumanStatistics)
