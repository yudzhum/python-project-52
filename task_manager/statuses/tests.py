from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class StatusesUrlsTest(TestCase):
    """Test that urls cannot be accessed without login"""
    def test_index_page_without_login(self):
        response = self.client.get(reverse('statuses:statuses'))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_create_page_without_login(self):
        response = self.client.get(reverse('statuses:create_status'))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_update_page_without_login(self):
        response = self.client.get(reverse('statuses:update_status', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_page_without_login(self):
        response = self.client.get(reverse('statuses:delete_status', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))


class StatusesTest(TestCase):
    """Test statuses CRUD"""
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
       self.user = CustomUser.objects.get(pk=1)
       self.client.force_login(self.user)
       self.new_data = {'name': 'brand new status'}

    def test_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:statuses'))
        self.assertEqual(response.status_code, 200) 

        statuses = Status.objects.all()
        self.assertQuerysetEqual(
            response.context['statuses'],
            statuses,
            ordered=False
        ) 

    def test_create_status(self):
        # GET page
        response = self.client.get(reverse('statuses:create_status'))
        self.assertEqual(response.status_code, 200)
        # Create status
        response = self.client.post(reverse('statuses:create_status'), self.new_data)
        new_status = Status.objects.last()
        self.assertEqual(new_status.name, self.new_data['name'])

    # Start from here
    def test_update(self):
        response = self.client.get(reverse('statuses:update_status', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 200)

    def test_delete_page_with_auth(self):
        response = self.client.get(reverse('statuses:delete_status', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 200)
