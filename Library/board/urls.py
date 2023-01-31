from django.urls import path
from .views import CommentApiView,ThreadApiView,ThreadFileUploadView,ThreadImageUploadView,ThreadFileGTView,ThreadImageGTView

urlpatterns = [
    path('thread/',ThreadApiView.as_view()),
    path('thread/<int:number>/',ThreadApiView.as_view()),
    #thread image post
    path('threadimage/upload/',ThreadImageUploadView.as_view()),
    #thread image get and delte
    path('threadimage/',ThreadImageGTView.as_view()),
    path('threadimage/<int:number>/',ThreadImageGTView.as_view()),
    #thread file post
    path('threadfile/upload/',ThreadFileUploadView.as_view()),
    #thread file get and delete
    path('threadfile/<int:number>/',ThreadFileGTView.as_view()),
    path('threadfile/',ThreadFileGTView.as_view()),
    
    path('comment/',CommentApiView.as_view()),
    path('comment/<int:number>/',CommentApiView.as_view()),
]