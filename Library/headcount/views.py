from django.shortcuts import render
from rest_framework.response import Response
from .models import Place,SubPlace,DailyCount
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import DPIsForAdmin
from django.utils.translation import gettext_lazy as _
from .serializers import PlaceSerializer,SubPlaceSerializer,DailyCountSerializer,AddDataDailyCount,PutDataDailyCount,AddSubPlaceSerializer,AddPlaceSerializer,PutPlaceSerializer
# Create your views here.


class PlaceAPIView(APIView):
    permission_classes=[IsAuthenticated,DPIsForAdmin]
    
    
    def get(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            queryset=Place.objects.all()
            serializer=PlaceSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=Place.objects.get(id=number)
                serializer=PlaceSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,**kwargs):
        serializer=AddPlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                ls=Place.objects.get(id=number)
            except Place.DoesNotExist:
                return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer=PutPlaceSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(number)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=Place.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)
        

class SubPlaceAPIView(APIView):
    permission_classes=[IsAuthenticated,DPIsForAdmin]
    
    
    def get(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            queryset=SubPlace.objects.all()
            serializer=SubPlaceSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=SubPlace.objects.get(id=number)
                serializer=SubPlaceSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,**kwargs):
        serializer=AddSubPlaceSerializer(data=request.data)
        if serializer.is_valid():
            ls=serializer.save()
            if ls.get('error') is None:
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(ls.get('error'),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=SubPlace.objects.get(id=number)
            serializer=SubPlaceSerializer(ls,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=SubPlace.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)
        
class DailyCountAPIVIew(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            queryset=DailyCount.objects.all()
            serializer=DailyCountSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=DailyCount.objects.get(id=number)
                serializer=DailyCountSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
    
    def post(self,request,**kwargs):
        serializer=AddDataDailyCount(data=request.data)
        if serializer.is_valid():
            ls=serializer.save(request.user)
            if ls.get('error') is None:
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(ls.get('error'),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=PutDataDailyCount(data=request.data)
            if serializer.is_valid():
                ls=serializer.save(number,request.user)
                if ls.get('error') is None:
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(ls.get('error'),status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
            
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=DailyCount.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)