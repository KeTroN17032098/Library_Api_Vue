from django.shortcuts import render
from rest_framework.response import Response
from .models import library_spot,member
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import LibrarySpotSerializer,MemberSerializer
from django.utils.translation import gettext_lazy as _
# Create your views here.


class AbstractModelAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def __init__(self,sc,mc):
        APIView.__init__(self)
        self.sc=sc
        self.MODEL_CLASSES=mc
    
    def get(self,request,**kwargs):
        number= kwargs.get('number') 
        if number is None:
            queryset=self.MODEL_CLASSES.objects.all()
            serializer=self.sc(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=self.MODEL_CLASSES.objects.get(id=number)
                serializer=self.sc(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,**kwargs):
        serializer=self.sc(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=self.MODEL_CLASSES.objects.get(id=number)
            serializer=self.sc(ls,data=request.data)
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
            ls=self.MODEL_CLASSES.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)

class LibrarySpotListAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,**kwargs):
        number= kwargs.get('number') 
        if number is None:
            queryset=library_spot.objects.all()
            serializer=LibrarySpotSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            queryset=library_spot.objects.get(id=number)
            serializer=LibrarySpotSerializer(queryset)
            return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=LibrarySpotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=library_spot.objects.get(id=number)
            serializer=LibrarySpotSerializer(ls,data=request.data)
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
            ls=library_spot.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)


class MemberAPIView(AbstractModelAPIView):
    def __init__(self):
        AbstractModelAPIView.__init__(self,MemberSerializer,member)