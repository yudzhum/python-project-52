from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.labels.models import Label
from task_manager.users.models import CustomUser


class LabelsUrlsTest(TestCase):
    """Test that urls cannot be accessed without login"""

    def test_index_page_without_login(self):
        response = self.client.get(reverse('labels:labels'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_page_without_login(self):
        response = self.client.get(reverse('labels:create_label'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_page_without_login(self):
        response = self.client.get(reverse('labels:update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_page_without_login(self):
        response = self.client.get(reverse('labels:delete_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class LabelTest(TestCase):
    """Test label CRUD"""

    fixtures = ['labels.json', 'users.json', 'tasks.json', 'statuses.json']

    def setUp(self):
        self.user = CustomUser.objects.get(pk=1)
        self.client.force_login(self.user)
        self.new_data = {'name': 'brand new label'}
        self.update_data = {'name': 'updated label'}

    def test_index_page(self):
        # self.client.force_login(self.user)
        response = self.client.get(reverse('labels:labels'))
        self.assertEqual(response.status_code, 200)

        labels = Label.objects.all()
        self.assertQuerysetEqual(
            response.context['labels'],
            labels,
            ordered=False
        )

    def test_create_label(self):
        # GET page
        response = self.client.get(reverse('labels:create_label'))
        self.assertEqual(response.status_code, 200)
        # Create label
        response = self.client.post(reverse('labels:create_label'), self.new_data, follow=True)
        self.assertRedirects(response, reverse('labels:labels'))
        new_label = Label.objects.last()
        self.assertEqual(new_label.name, self.new_data['name'])

    def test_update_label(self):
        # GET page
        response = self.client.get(reverse('labels:update_label', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        # Update label
        response = self.client.post(
            reverse('labels:update_label', kwargs={'pk': 1}),
            self.update_data,
            follow=True
        )
        self.assertRedirects(response, reverse('labels:labels'))
        updated_label = Label.objects.get(pk=1)
        self.assertEqual(updated_label.name, self.update_data['name'])

    def test_delete_label(self):
        # GET page
        label = Label.objects.last()
        response = self.client.get(reverse('labels:delete_label', kwargs={'pk': label.pk}))
        self.assertEqual(response.status_code, 200)
        # Delete label
        response = self.client.post(reverse('labels:delete_label', kwargs={'pk': label.pk}))
        self.assertRedirects(response, reverse('labels:labels'))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=label.pk)

    def test_delete_label_linked_to_task(self):
        # GET page
        response = self.client.get(reverse('labels:delete_label', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        # Attemp to delete label
        response = self.client.post(reverse('labels:delete_label', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('labels:labels'))
        # Object exist
        self.assertTrue(Label.objects.get(pk=2))
