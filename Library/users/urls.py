from django.urls import path, include,re_path
from rest_auth.registration.views import VerifyEmailView,RegisterView
from .views import CConfirmEmailView,CustomResendEmailVerification
from .views import google_callback,google_login,GoogleLogin
from .views import KakaoSocialLoginMethodSet,KakaoLogin
from .views import NaverSocialLoginMethodSet,NaverLogin,SocialLoginForSPA

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
    path('registration/resend-email/', CustomResendEmailVerification.as_view(), name="rest_resend_email"),
    #google social login
    path('sociallogin/google/login/',google_login,name='google_login'),
    path('sociallogin/google/callback/',google_callback,name='google_callback'),
    path('sociallogin/google/finish/',GoogleLogin.as_view(), name='google_login_todjango'),
    #kakao social login
    path('sociallogin/kakao/login/',KakaoSocialLoginMethodSet.kakao_login,name='kakao_login'),
    path('sociallogin/kakao/callback/',KakaoSocialLoginMethodSet.kakao_callback,name='kakao_callback'),
    path('sociallogin/kakao/finish/',KakaoLogin.as_view(), name='kakao_login_todjango'),
    #naver social login
    path('sociallogin/naver/login/',NaverSocialLoginMethodSet.naver_login,name='naver_login'),
    path('sociallogin/naver/callback/',NaverSocialLoginMethodSet.naver_callback,name='naver_callback'),
    path('sociallogin/naver/finish/',NaverLogin.as_view(), name='naver_login_todjango'),

    path('sociallogin/SPA',SocialLoginForSPA.as_view(), name='spa_sociallogin'),
]
