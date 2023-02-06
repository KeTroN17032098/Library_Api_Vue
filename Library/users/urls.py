from django.urls import path, include,re_path
from rest_auth.registration.views import VerifyEmailView,RegisterView
from .views import CConfirmEmailView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('',include('allauth.urls')),
        re_path(r'^registration/account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 유저가 클릭한 이메일(=링크) 확인
        re_path(
        r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', CConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    path('registration/', RegisterView.as_view(), name='accoutn_registeration'),


]
