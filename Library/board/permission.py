from rest_framework import permissions
from django.conf import Settings

class OwnerandAdminCanRewrite(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method not in (permissions.SAFE_METHODS and 'POST'):
            return (request.user.is_staff or obj.created_by==request.user)
        else:
            return True