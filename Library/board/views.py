from django.shortcuts import render
from rest_framework.response import Response
from .models import Thread,Comment,ThreadFile,ThreadImage
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser
from .permission import OwnerandAdminCanRewrite
from django.utils.translation import gettext_lazy as _
from .serilaizers import PostCommentSerializer,PPThreadSerializer,PutCommentSerializer,GetThreadSerializer,GetCommentSerializer,ThreadFilesSerializer,ThreadImagesSerializer
from Library.pagination import PaginationHandlerMixin,DefaultResultsSetPagination
# Create your views here.

class ThreadFileUploadView(APIView):
    permission_classes =[IsAuthenticated,OwnerandAdminCanRewrite]
    parser_classes=[FileUploadParser]
    def post(self, request):
        if not 'threadid' in request.GET:
            return Response(_("No Thread ID"),status=status.HTTP_400_BAD_REQUEST)
        threadid=request.GET['threadid']
        thread=Thread.objects.get(id=threadid)
        if thread is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            threadfile=ThreadFile.objects.create(thread=thread,file=request.data.get('file'))
            return Response(threadfile.__str__(),status=status.HTTP_201_CREATED)

class ThreadImageUploadView(APIView):
    permission_classes =[IsAuthenticated,OwnerandAdminCanRewrite]
    parser_classes=[FileUploadParser]
    def post(self, request):
        if not 'threadid' in request.GET:
            return Response(_("No Thread ID"),status=status.HTTP_400_BAD_REQUEST)
        threadid=request.GET['threadid']
        thread=Thread.objects.get(id=threadid)
        if thread is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            threadfile=ThreadImage.objects.create(thread=thread,image=request.data.get('file'))
            return Response(threadfile.__str__(),status=status.HTTP_201_CREATED)    
            
class ThreadFileGTView(APIView):
    def get(self, request,**kwargs):
        number = kwargs.get('number')
        if number is None:
            queryset=ThreadFile.objects.all()
            serializer=ThreadFilesSerializer(instance=queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=ThreadFile.objects.get(id=number)
                serializer=ThreadFilesSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
            
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=ThreadFile.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)

class ThreadImageGTView(APIView):
    permission_classes =[IsAuthenticated,OwnerandAdminCanRewrite]

    def get(self, request,**kwargs):
        number = kwargs.get('number')
        if number is None:
            queryset=ThreadImage.objects.all()
            serializer=ThreadImagesSerializer(instance=queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=ThreadImage.objects.get(id=number)
                serializer=ThreadImagesSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
            
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=ThreadImage.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)

class ThreadApiView(APIView,PaginationHandlerMixin):
    permission_classes =[IsAuthenticated,OwnerandAdminCanRewrite]
    pagination_class=DefaultResultsSetPagination
    
    def get(self, request,**kwargs):
        number = kwargs.get('number')
        if number is None:
            queryset=Thread.objects.all()
            page=self.paginate_queryset(queryset)
            if page is None:
                serializer=GetThreadSerializer(queryset,many=True)
            else:
                serializer=self.get_paginated_response(GetThreadSerializer(page,many=True).data)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=Thread.objects.get(id=number)
                serializer=GetThreadSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
            
    def post(self,request,**kwargs):
        serializer=PPThreadSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save(request.user,0,'POST'):
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=PPThreadSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.save(request.user,number,'PUT'):
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=Thread.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)
        
class CommentApiView(APIView):
    permission_classes =[IsAuthenticated,OwnerandAdminCanRewrite]
    
    def get(self, request,**kwargs):
        number = kwargs.get('number')
        if number is None:
            queryset=Comment.objects.all()
            serializer=GetCommentSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            try:
                queryset=Comment.objects.get(id=number)
                serializer=GetCommentSerializer(queryset)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Exception as e:
                return Response(str(e),status=status.HTTP_404_NOT_FOUND)
            
    def post(self,request,**kwargs):
        serializer=PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.save(request.user):
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,**kwargs):
        number=kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer=PutCommentSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.save(request.user,number):
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,**kwargs):
        number= kwargs.get('number')
        if number is None:
            return Response(_("Invalid Request"),status=status.HTTP_400_BAD_REQUEST)
        else:
            ls=Comment.objects.get(id=number)
            ls.delete()
            return Response(_("Delete Completed"),status.HTTP_200_OK)