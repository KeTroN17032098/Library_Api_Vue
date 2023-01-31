from rest_framework import serializers
from .models import Place,SubPlace,DailyCount
from users.serializers import UserInfoSerializer
from django.utils.translation import gettext_lazy as _

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields='__all__'
        
class SubPlaceSerializer(serializers.ModelSerializer):
    place=PlaceSerializer(read_only=True)
    class Meta:
        model=SubPlace
        fields='__all__'
        
class DailyCountSerializer(serializers.ModelSerializer):
    subplace=SubPlaceSerializer(read_only=True)
    created_by=UserInfoSerializer(read_only=True)
    modified_by=UserInfoSerializer(read_only=True)
    class Meta:
        model=DailyCount
        fields='__all__'
        
class AddPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields=['name',]
        
class PutPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields=['name',]
    
    def save(self,id):
        place=Place.objects.get(id=id)
        place.name=self.validated_data['name']
        place.save()
        
class AddSubPlaceSerializer(serializers.Serializer):
    placename=serializers.CharField(max_length=255)
    subplacename=serializers.CharField(max_length=255)
    def save(self):
        ls={}
        try:
            place=Place.objects.get(name=self.validated_data['placename'])
            subplace=SubPlace.objects.get(name=self.validated_data['subplacename'],place=place.pk)
        except Place.DoesNotExist:
            ls['error']=_("Certain Place does not exist.")
        except SubPlace.DoesNotExist:
            subplace=SubPlace(place=place,name=self.validated_data['subplacename'])
            subplace.save()
        else:
            ls['error']=_("Already Exist")
        finally:
            return ls

            
            
class AddDataDailyCount(serializers.Serializer):
    placename=serializers.CharField(max_length=255)
    subplacename=serializers.CharField(max_length=255)
    date=serializers.DateField()
    malecount=serializers.IntegerField()
    femalecount=serializers.IntegerField()
    def save(self,user):
        ls={}
        dt=self.validated_data['date']
        mc=self.validated_data['malecount']
        fc=self.validated_data['femalecount']
        try:
            place=Place.objects.get(name=self.validated_data['placename'])
            subplace=SubPlace.objects.get(name=self.validated_data['subplacename'],place=place.pk)
            dailycount=DailyCount.objects.get(subplace=subplace.pk,date=dt)
        except Place.DoesNotExist:
            ls['error']=_("Certain Place does not exist.")
        except SubPlace.DoesNotExist:
            ls['error']=_("Certain Subplace does not exist.")
        except DailyCount.DoesNotExist:
            dailycount=DailyCount(subplace=subplace,date=dt,male=mc,female=fc,created_by=user,modified_by=user)
            dailycount.save()
        except Exception as e:
            print(e)
        else:
            dailycount.male=dailycount.male+max(mc,0)
            dailycount.female=dailycount.female+max(fc,0)
            dailycount.modified_by=user
            dailycount.save()
        finally:
            return ls

            
    
class PutDataDailyCount(serializers.Serializer):
    malecount=serializers.IntegerField()
    femalecount=serializers.IntegerField()
    
    def save(self,number,user):
        ls={}
        mc=max(self.validated_data['malecount'],0)
        fc=max(self.validated_data['femalecount'],0)
        try:
            dc=DailyCount.objects.get(id=number)
            dc.male=dc.male+mc
            dc.female=dc.female+fc
            dc.modified_by=user
            dc.save()
        except DailyCount.DoesNotExist:
            ls['error']=_("Certain DailyCount does not exist.")
        except Exception as e:
            print(e)
        finally:
            return ls