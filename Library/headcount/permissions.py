from rest_framework import permissions
from django.conf import Settings

class DPIsForAdmin(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in ('DELETE','PUT'):
            return request.user.is_staff
        else:
            return True
        
