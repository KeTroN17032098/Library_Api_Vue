# views.py
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from dj_rest_auth.registration.serializers import ResendEmailVerificationSerializer
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.naver import views as naver_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from json.decoder import JSONDecodeError


class CConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):

        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return Response(_("Email Verified"), status=status.HTTP_200_OK)

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                return Response(_("Email Not Exist"), status=status.HTTP_400_BAD_REQUEST)
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


class CustomResendEmailVerification(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = EmailAddress.objects.filter(
            **serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)
            return Response(_("Resend"), status=status.HTTP_200_OK)
        else:
            return Response(_("Email Not Exist"), status=status.HTTP_400_BAD_REQUEST)


state = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/v1/sociallogin/google/callback/'
GOOGLE_FINISH_URL = BASE_URL+'api/accounts/v1/sociallogin/google/finish/'
google_scope = "https://www.googleapis.com/auth/userinfo.email"
google_client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
google_client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
KAKAO_CALLBACK_URI = BASE_URL+'api/accounts/v1/sociallogin/kakao/callback/'
kakao_client_id = getattr(settings, 'SOCIAL_AUTH_KAKAO_CLIENT_ID')
KAKAO_FINSH_URL = BASE_URL+'api/accounts/v1/sociallogin/kakao/finish/'
NAVER_CALLBACK_URI = BASE_URL+'api/accounts/v1/sociallogin/naver/callback/'
NAVER_FINSH_URL = BASE_URL+'api/accounts/v1/sociallogin/naver/finish/'
naver_client_id = getattr(settings, 'SOCIAL_AUTH_NAVER_CLIENT_ID')
naver_client_secret = getattr(settings, 'SOCIAL_AUTH_NAVER_SECRET')


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return HttpResponseRedirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")

    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    email_req_json = email_req.json()
    email = email_req_json.get('email')
    """
    Signup or Signin Request
    """
    try:
        print(email)
        user = User.objects.get(email=email)
        print(user)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': _('no matching social type')}, status=status.HTTP_400_BAD_REQUEST)
        if social_user == None:
            return JsonResponse({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(GOOGLE_FINISH_URL, data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()

        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(GOOGLE_FINISH_URL, data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            print(accept_status)
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()

        return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


class KakaoSocialLoginMethodSet:

    def kakao_login(request):
        return HttpResponseRedirect(f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email")

    def kakao_callback(request):
        """
        Get Access Token
        """
        code = request.GET.get('code')
        token_request = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={kakao_client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
        trj = token_request.json()
        error = trj.get('error', None)
        if error is not None:
            raise JSONDecodeError(error)
        access_token = trj.get('access_token', None)
        """
        Get Email
        """
        pr = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers={'Authorization': f"Bearer {access_token}"}
        )
        prj = pr.json()
        ka = prj.get('kakao_account')
        email = ka.get('email', None)
        if email is None:
            return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(email)
            user = User.objects.get(email=email)
            # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
            # 다른 SNS로 가입된 유저
            social_user = SocialAccount.objects.get(user=user)
            if social_user.provider != 'kakao':
                return JsonResponse({'err_msg': _('no matching social type')}, status=status.HTTP_400_BAD_REQUEST)
            if social_user == None:
                return JsonResponse({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)
            # 기존에 Google로 가입된 유저
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(KAKAO_FINSH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()

            return JsonResponse(accept_json)
        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(KAKAO_FINSH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                print(accept_status)
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            accept_json = accept.json()

            return JsonResponse(accept_json)
        except SocialAccount.DoesNotExist:
            return JsonResponse({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client


class NaverSocialLoginMethodSet:

    def naver_login(request):
        return HttpResponseRedirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={naver_client_id}&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URI}")

    def naver_callback(request):
        """
        Get Access Token
        """
        state_string = request.GET.get('state')
        code = request.GET.get('code')
        token_request = requests.post(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver_client_id}&client_secret={naver_client_secret}&code={code}&state={state_string}")
        trj = token_request.json()
        error = trj.get('error', None)
        if error is not None:
            raise JSONDecodeError(error)
        access_token = trj.get('access_token', None)
        """
        Get Email
        """
        pr = requests.post(
            "https://openapi.naver.com/v1/nid/me",
            headers={'Authorization': f"Bearer {access_token}"}
        )
        prj = pr.json()
        email = prj.get('response').get('email')
        if email is None:
            return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            print(email)
            user = User.objects.get(email=email)
            # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
            # 다른 SNS로 가입된 유저
            social_user = SocialAccount.objects.get(user=user)
            if social_user.provider != 'naver':
                return JsonResponse({'err_msg': _('no matching social type')}, status=status.HTTP_400_BAD_REQUEST)
            if social_user == None:
                return JsonResponse({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)
            # 기존에 Google로 가입된 유저
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(NAVER_FINSH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()

            return JsonResponse(accept_json)
        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            data = {'access_token': access_token, 'code': code}
            print(data)
            accept = requests.post(NAVER_FINSH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                print(accept_status)
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            accept_json = accept.json()

            return JsonResponse(accept_json)
        except SocialAccount.DoesNotExist:
            return JsonResponse({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)


class NaverLogin(SocialLoginView):
    adapter_class = naver_view.NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client


class SocialLoginForSPA(APIView):
    def get(self, request):
        provider = request.GET.get('provider')
        data = []
        if provider is None:
            return Response(_("No provider specified"), status=status.HTTP_400_BAD_REQUEST)
        elif provider.lower() == 'naver':
            data['url'] = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={naver_client_id}&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URI}"
        elif provider.lower() == 'kakao':
            data['url'] = f"https://kauth.kakao.com/oauth/authorize?client_id={kakao_client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email"
        elif provider.lower() == "google":
            data['url'] = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={google_scope}"
        else:
            return Response(_("Unsupported provider specified"), status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        provider = request.GET.get('provider')
        data = []
        if provider is None:
            return Response(_("No provider specified"), status=status.HTTP_400_BAD_REQUEST)
        state_string = request.GET.get('state')
        code = request.GET.get('code')
        token_url = ''
        if provider.lower() == 'naver':
            token_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver_client_id}&client_secret={naver_client_secret}&code={code}&state={state_string}"
        elif provider.lower() == 'kakao':
            token_url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={kakao_client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}"
        elif provider.lower() == "google":
            token_url = f"https://oauth2.googleapis.com/token?client_id={google_client_id}&client_secret={google_client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
        else:
            return Response(_("Unsupported provider specified"), status=status.HTTP_400_BAD_REQUEST)
        token_request = requests.post(token_url)
        trj = token_request.json()
        error = trj.get('error', None)
        if error is not None:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        access_token = trj.get('access_token', None)
        if provider.lower() == 'naver':
            pr = requests.post(
                "https://openapi.naver.com/v1/nid/me",
                headers={'Authorization': f"Bearer {access_token}"}
            )
            email = prj.get('response').get('email')
            FINISH_URL=NAVER_FINSH_URL
        elif provider.lower() == 'kakao':
            pr = requests.post(
                "https://kapi.kakao.com/v2/user/me",
                headers={'Authorization': f"Bearer {access_token}"}
            )
            prj = pr.json()
            ka = prj.get('kakao_account')
            email = ka.get('email', None)
            FINISH_URL=KAKAO_FINSH_URL
        elif provider.lower() == "google":
            email_req = requests.get(
                f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
            email_req_status = email_req.status_code
            if email_req_status != 200:
                return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

            email_req_json = email_req.json()
            email = email_req_json.get('email')
            FINISH_URL=GOOGLE_FINISH_URL
        try:
            print(email)
            user = User.objects.get(email=email)
            print(user)
            # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
            # 다른 SNS로 가입된 유저
            social_user = SocialAccount.objects.get(user=user)
            if social_user.provider != 'google':
                return Response({'err_msg': _('no matching social type')}, status=status.HTTP_400_BAD_REQUEST)
            if social_user == None:
                return Response({'err_msg': _('email exists but not social user')}, status=status.HTTP_400_BAD_REQUEST)
            # 기존에 Google로 가입된 유저
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(FINISH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return Response({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()
            return Response(accept_json,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 새로 가입
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(FINISH_URL, data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                print(accept_status)
                return Response({'err_msg': 'failed to signup'}, status=accept_status)
            accept_json = accept.json()
            return Response(accept_json, status=status.HTTP_201_CREATED)
