from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from task_manager.utils import get_test_data
from task_manager.users.models import CustomUser

app_name = 'users'


class UsersTest(TestCase):
    """Test user CRUD"""
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data(app_name, 'test_data.json')

    def assertCustomUser(self, created_user, new_user_data):
        self.assertEqual(created_user.username, new_user_data['username'])
        self.assertEqual(created_user.first_name, new_user_data['first_name'])
        self.assertEqual(created_user.last_name, new_user_data['last_name'])

    def test_users_index_page(self):
        response = self.client.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)

        users = CustomUser.objects.all()
        self.assertQuerysetEqual(
            response.context['user_list'],
            users,
            ordered=False
        )
 
    def test_register_page(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        new_user = self.test_data['new_user']
        response = self.client.post(reverse('users:register'), new_user)

        self.assertRedirects(response, reverse('login'))
        created_user = CustomUser.objects.get(username=new_user['username'])
        self.assertCustomUser(created_user, new_user)


    def test_update_page(self):
        pre_update_data = self.test_data['user_before_update']
        user_pre_update = CustomUser.objects.get(username=pre_update_data['username'])
        response = self.client.get(reverse('users:update_user', args=[user_pre_update.pk]))

        self.assertEqual(response.status_code, 200)
