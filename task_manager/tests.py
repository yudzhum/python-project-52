from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import CustomUser


class IndexTest(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user = CustomUser.objects.get(pk=1)
        self.login_data = {
            'username': self.user.username,
            'password': self.user.password
        }

        self.login_user = CustomUser.objects.get(pk=2)

    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('login'), self.login_data, follow=True)
        self.assertTrue(self.user.is_authenticated)

    def test_logout(self):
        self.client.force_login(self.login_user)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
