from django.contrib import admin
from .models import Thread,Comment,ThreadImage,ThreadFile
# Register your models here.

admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(ThreadImage)
admin.site.register(ThreadFile)