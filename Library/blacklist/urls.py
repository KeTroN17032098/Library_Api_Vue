from django.urls import path
from .views import LibrarySpotListAPI,MemberAPIView

urlpatterns = [
    path('Library_Spot/',LibrarySpotListAPI.as_view()),
    path('Library_Spot/<int:number>/',LibrarySpotListAPI.as_view()),
     path('member/',MemberAPIView.as_view()),
    path('member/<int:number>/',MemberAPIView.as_view()),
]