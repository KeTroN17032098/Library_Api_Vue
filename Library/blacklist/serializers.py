from rest_framework import serializers
from .models import library_spot,member

class LibrarySpotSerializer(serializers.ModelSerializer):
    class Meta:
        model=library_spot
        fields='__all__'

class MemberSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    where =serializers.PrimaryKeyRelatedField(queryset=library_spot.objects.all(),many=True)
    
    class Meta:
        model=member
        fields=('name','libraryid','count','where','description',)
