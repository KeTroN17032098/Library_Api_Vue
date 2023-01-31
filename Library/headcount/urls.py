from django.urls import path
from .views import PlaceAPIView,SubPlaceAPIView,DailyCountAPIVIew

urlpatterns = [
    path('place/',PlaceAPIView.as_view()),
    path('place/<int:number>/',PlaceAPIView.as_view()),
    path('subplace/',SubPlaceAPIView.as_view()),
    path('subplace/<int:number>/',SubPlaceAPIView.as_view()),
    path('dailycount/',DailyCountAPIVIew.as_view()),
    path('dailycount/<int:number>/',DailyCountAPIVIew.as_view()),
]