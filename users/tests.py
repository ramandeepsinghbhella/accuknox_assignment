from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword', name='Test User')
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_signup(self):
        url = reverse('signup')
        data = {'email': 'newuser@example.com', 'password': 'newpassword', 'name': 'New User'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        data = {'email': 'testuser@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_search(self):
        url = reverse('user_search') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_friend_request(self):
        new_user = User.objects.create_user(email='anotheruser@example.com', password='anotherpassword', name='Another User')
        url = reverse('send_friend_request')
        data = {'to_user': new_user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_friends(self):
        url = reverse('list_friends')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pending_friend_requests(self):
        url = reverse('pending_friend_requests')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
