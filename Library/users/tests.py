from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from .models import User
# Create your tests here.

class UserAuthAPIViewTestCase(APITestCase):
    def setUp(self):
        self.data={
            "email":"sample@example.com",
            "password":"sample1234"
        }
        self.user=User.objects.create_user("sample@example.com","sample1234")
        self.user.verified=True
        self.user.save()
        
        print("created : "+self.user.email)
    
    def test_registeration(self):
        url=reverse('accoutn_registeration')
        user_data={
            "username":"",
            "email":"sample2@example.com",
            "password1":"sample1234",
            "password2":"sample1234"
        }
        response=self.client.post(url,user_data)
        self.assertEqual(response.status_code,201)
        
    def test_login(self):
        url=reverse('rest_login')
        user_data={
            "email":"sample@example.com",
            "password":"sample1234"
        }
        response=self.client.post(url,user_data)
        print(response.data)
        self.assertEqual(response.status_code,200)