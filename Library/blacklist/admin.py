from django.contrib import admin
from .models import member,library_spot
# Register your models here.
admin.site.register(library_spot)
admin.site.register(member)