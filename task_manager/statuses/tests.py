from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

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
        response = self.client.get(reverse('statuses:update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_page_without_login(self):
        response = self.client.get(reverse('statuses:delete_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class StatusesTest(TestCase):
    """
    Test statuses CRUD,
    user is authorized
    """
    fixtures = ['statuses.json', 'users.json', 'tasks.json']

    def setUp(self):
        self.user = CustomUser.objects.get(pk=1)
        self.client.force_login(self.user)
        self.new_data = {'name': 'brand new status'}
        self.update_data = {'name': 'updated status'}

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

    def test_update_status(self):
        # GET page
        response = self.client.get(reverse('statuses:update_status', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        # Update status
        response = self.client.post(
            reverse('statuses:update_status', kwargs={'pk': 1}),
            self.update_data
        )
        updated_status = Status.objects.get(pk=1)
        self.assertEqual(updated_status.name, self.update_data['name'])

    def test_delete_status(self):
        # GET page
        response = self.client.get(reverse('statuses:delete_status', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        # DElete status
        response = self.client.post(reverse('statuses:delete_status', kwargs={'pk': 3}))
        self.assertRedirects(response, reverse('statuses:statuses'))
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=3)

    def test_delete_status_linked_to_task(self):
        # GET page
        response = self.client.get(reverse('statuses:delete_status', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        # Attemp to delete status
        response = self.client.post(reverse('statuses:delete_status', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('statuses:statuses'))
        # Object exist
        self.assertTrue(Status.objects.get(pk=2))
