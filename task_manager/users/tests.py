from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.utils import get_test_data
from task_manager.users.models import CustomUser


# Do something with magic numbers in pk
class UsersTest(TestCase):
    """Test users CRUD"""
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data('test_data_for_users.json')

    def assertCustomUser(self, user, user_data):
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])

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

    def test_update_page_redirect_if_not_logged_in(self):
        user = CustomUser.objects.get(pk=3)
        response = self.client.get(reverse('users:update_user', kwargs={'pk': user.pk}))
        # Manually check redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update(self):
        # Log in user
        user = CustomUser.objects.get(pk=3)
        self.client.force_login(user)
        # GET page
        response = self.client.get(reverse('users:update_user', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 200)
        # update user
        new_data = self.test_data['user_after_update']
        response = self.client.post(
            reverse('users:update_user', kwargs={'pk': user.pk}),
            new_data
        )
        updated_user = CustomUser.objects.get(pk=user.pk)
        self.assertRedirects(response, reverse('users:users'))
        self.assertCustomUser(updated_user, new_data)

    def test_update_without_permission(self):
        # Log in user
        user = CustomUser.objects.get(pk=3)
        self.client.force_login(user)
        # Try GET update page of different user
        response = self.client.get(reverse('users:update_user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)

    def test_delete_page_redirect_if_not_logged_in(self):
        user = CustomUser.objects.get(pk=4)
        response = self.client.get(reverse('users:delete_user', kwargs={'pk': user.pk}))
        # Manually check redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_user(self):
        # Log in user
        user = CustomUser.objects.get(pk=4)
        self.client.force_login(user)
        # GET page
        response = self.client.get(reverse('users:delete_user', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 200)
        # delete user
        response = self.client.post(reverse('users:delete_user', kwargs={'pk': user.pk}))
        self.assertRedirects(response, reverse('users:users'))
        with self.assertRaises(ObjectDoesNotExist):
            CustomUser.objects.get(pk=4)

    def test_delete_without_permission(self):
        # Log in user
        user = CustomUser.objects.get(pk=3)
        self.client.force_login(user)
        # Try GET page of different user
        response = self.client.get(reverse('users:update_user', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
