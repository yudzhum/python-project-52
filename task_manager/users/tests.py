from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.urls import reverse_lazy

from task_manager.utils import get_test_data
from task_manager.users.models import CustomUser

app_name = 'users'


class UsersTest(TestCase):
    """Test users index page and registration"""
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data(app_name, 'test_data.json')

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


class UpdateAndDeleteUserTest(TestCase):
    """
    Test updation and delete of user.
    Both requeire login.
    Only owner can delete user account.
    """

    @classmethod
    def setUp(cls):
        test_user1 = CustomUser.objects.create(
            username='testuser1',
            first_name='kara',
            last_name='denvers',
            password='1234'
        )
        test_user1.save()


    def test_users_index_page(self):
        response = self.client.get(reverse('users:users'))
        self.assertEqual(response.status_code, 200)

        users = CustomUser.objects.count()
        assert users == 1

    
    def test_redirect_if_not_logged_in(self):
        user = CustomUser.objects.get(username='catco')
        response = self.client.get(reverse('users:update_user', kwargs={'pk': user.pk }))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


    def test_update_page(self):
        login = self.client.login(username='testuser1', password='1234')
        self.assertTrue(login) 



    # def test_update(self):
    #     pre_update_data = self.test_data['user_before_update']
    #     new_data = self.test_data['user_after_update']
    #     user_pre_update = CustomUser.objects.get(username=pre_update_data['username'])
    #     response = self.client.post(reverse(
    #         'users:update_user', args=[user_pre_update.pk]),
    #         new_data
    #     )
    #     self.assertRedirects(response, reverse('users:users'))
    #     updated_user = CustomUser.objects.get(pk=user_pre_update.pk)
    #     self.assertCustomUser(updated_user, new_data)
