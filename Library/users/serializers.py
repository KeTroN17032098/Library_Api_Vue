from rest_framework import serializers
from .models import User
from django.utils.translation import gettext_lazy as _

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','email','is_staff']