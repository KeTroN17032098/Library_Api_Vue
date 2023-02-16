from rest_framework import serializers
from users.serializers import UserInfoSerializer
from django.utils.translation import gettext_lazy as _
from .models import Thread,Comment,ThreadFile,ThreadImage

class ThreadFilesSerializer(serializers.ModelSerializer):
    file=serializers.FileField(use_url=True)
    
    class Meta:
        model=ThreadFile
        fields=['file']
        
class ThreadImagesSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(use_url=True)
    
    class Meta:
        model=ThreadImage
        fields=['image']

class GetThreadCommentsSerializer(serializers.ModelSerializer):
    body=serializers.CharField(read_only=True)
    created_by=UserInfoSerializer(read_only=True)
    modified_by=UserInfoSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=['body','created_by','modified_by','created_on','modified_on']


class GetThreadSerializer(serializers.ModelSerializer):
    images=serializers.SerializerMethodField()
    files=serializers.SerializerMethodField()
    created_by=UserInfoSerializer(read_only=True)
    modified_by=UserInfoSerializer(read_only=True)
    comments=GetThreadCommentsSerializer(source='comment_set',many=True,read_only=True)
    class Meta:
        model = Thread
        fields =['id','title','body','images','files','created_by','modified_by','created_on','modified_on','comments']
    
    def get_images(self,obj):
        image=obj.threadimage_set.all()
        return ThreadImagesSerializer(instance=image,many=True,context=self.context).data

    def get_files(self,obj):
        file=obj.threadfile_set.all()
        return ThreadFilesSerializer(instance=file,many=True,context=self.context).data

        
class PPThreadSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=100)
    body=serializers.CharField()
    def save(self,user,number,type):
        td=self.validated_data['title']
        bd=self.validated_data['body']
        if type=='POST':
            thread=Thread(title=td,body=bd,created_by=user,modified_by=user)
            thread.save()
            return True
        elif type=='PUT':
            try:
                thread=Thread.objects.get(id=number)
            except Thread.DoesNotExist:
                return False
            else:
                thread.title=td;
                thread.body=bd;
                thread.modified_by=user
                thread.save()
                return True

class GetCommentSerializer(serializers.ModelSerializer):
    thread=GetThreadSerializer(read_only=True)
    created_by=UserInfoSerializer(read_only=True)
    modified_by=UserInfoSerializer(read_only=True)
    class Meta:
        model=Comment
        fields='__all__'
        
class PostCommentSerializer(serializers.Serializer):
    threadid=serializers.IntegerField()
    body=serializers.CharField()
    def save(self,user):
        tid=self.validated_data['threadid']
        bd=self.validated_data['body']
        try:
            thread=Thread.objects.get(id=tid)
        except Thread.DoesNotExist:
            return False
        else:
            comment=Comment(thread=thread,body=bd,created_by=user,modified_by=user)
            comment.save()
            return True
        
class PutCommentSerializer(serializers.Serializer):
    body=serializers.CharField()
    def save(self,user,number):
        bd=self.validated_data['body']
        try:
            comment=Comment.objects.get(id=number)
        except Comment.DoesNotExist:
            return False
        else:
            comment.body=bd
            comment.modified_by=user
            comment.save()
            return True
    