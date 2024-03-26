from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# from watch_list.api import serializers
from watch_list import models


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase",password="NewPassword@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name= "Netflix",
            about= "OTT Platform",
            website= "http://netflix.com")
        
        
    def test_streamplatform_create(self):
        data={
            "name": "Netflix",
            "about": "OTT Platform",
            "website": "http://netflix.com"
            
        }
        response = self.client.post(reverse('stream_platform'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        
        response = self.client.get(reverse('stream_platform'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_streamplatform_detail(self):
        
        response = self.client.get(reverse('stream_detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
class WatchListTestCase(APITestCase):
    
    def setUp(self):
        def setUp(self):
            self.user = User.objects.create_user(username="testcase",password="NewPassword@123")
            self.token = Token.objects.get(user__username=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name= "Netflix",
            about= "OTT Platform",
            website= "http://netflix.com")
        
        self.watchlist = models.WatchList.objects.create(platform= self.stream,
            title= "example",
            storyline= "story",
            active= True)
        
    
    def test_watchlist_create(self):
        
        data= {
            "platform": self.stream,
            "title": "example",
            "storyline": "story",
            "active": True
        }
        response = self.client.post(reverse('watch_list'),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_watchlist_list(self):
        
        response = self.client.get(reverse('watch_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        
        response = self.client.get(reverse('watch_detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'example')
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="testcase",password="NewPassword@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
        self.stream = models.StreamPlatform.objects.create(name= "Netflix",
            about= "OTT Platform",
            website= "http://netflix.com")
        
        self.watchlist = models.WatchList.objects.create(platform= self.stream,
            title= "example",
            storyline= "story",
            active= True)
        
        self.watchlist2 = models.WatchList.objects.create(platform= self.stream,
            title= "example",
            storyline= "story",
            active= True)
        
        self.review=models.Review.objects.create(review_user = self.user,
            rating= 5,
            description= "Great Movie",
            watchlist= self.watchlist,
            active= True)
        
    def test_review_create(self):
        
        data={
            "review_user":self.user,
            "rating": 5,
            "description": "Great Movie",
            "watchlist": self.watchlist2,
            "active": True
        }
        
        response = self.client.post(reverse('review_create', args=(self.watchlist2.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
    
        
        response = self.client.post(reverse('review_create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_review_create_unauth(self):
        
        data={
            "review_user":self.user,
            "rating": 5,
            "description": "Great Movie",
            "watchlist": self.watchlist,
            "active": True
        }
        
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review_create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        
        data={
            "review_user":self.user,
            "rating": 4,
            "description": "Great Movie - Updated",
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('review_detail', args=(self.review.id,)),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_list(self):
        response = self.client.get(reverse('review_list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_detail(self):
        response = self.client.get(reverse('review_detail',args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_review_delete(self):
        response = self.client.delete(reverse('review_detail',args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    
        
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username'+ self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
        
    
        
        
        
        
        