from django.contrib import admin
from .models import Place,SubPlace,DailyCount
# Register your models here.

admin.site.register(Place)
admin.site.register(SubPlace)
admin.site.register(DailyCount)