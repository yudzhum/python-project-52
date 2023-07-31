from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from task_manager.tasks.models import Task
from task_manager.users.models import CustomUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskUrlsTest(TestCase):
    """Test that urls cannot be accessed without login"""

    def test_index_page_without_login(self):
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_create_task_page_without_login(self):
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_update_task_page_without_login(self):
        response = self.client.get(reverse('tasks:update_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_task_page_without_login(self):
        response = self.client.get(reverse('tasks:delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_show_task_page_without_login(self):
        response = self.client.get(reverse('tasks:show_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))


class TaskTest(TestCase):
    """
    Test task CRUD,
    user is authorized
    """
    fixtures = [
        'tasks.json',
        'users.json',
        'statuses.json',
        'labels.json'
    ]

    def setUp(self):
        self.user_author = CustomUser.objects.get(pk=1)
        self.client.force_login(self.user_author)

        self.user_executor = CustomUser.objects.get(pk=2)

        self.status = Status.objects.get(pk=1)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

        self.new_data = {
            "name": "Drink water",
            "description": "",
            "status": self.status.pk,
            "executor": self.user_executor.pk,
            "labels": [self.label1.pk]
        }

        self.update_data = {
            "name": "Update task and test it",
            "description": "test text",
            "status": self.status.pk,
            "executor": self.user_executor.pk,
            "labels": [self.label2.pk]
        }

    def assertTask(self, task, task_data):
        self.assertEqual(task.name, task_data['name'])
        self.assertEqual(task.description, task_data['description'])
        self.assertEqual(task.status, Status.objects.get(pk=task_data['status']))
        self.assertEqual(task.executor, CustomUser.objects.get(pk=task_data['executor']))

    def test_index_page(self):
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.all()
        self.assertQuerysetEqual(
            response.context['taskslist'],
            tasks,
            ordered=False
        )

    def test_task_page(self):
        task = Task.objects.last()
        response = self.client.get(reverse('tasks:show_task', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        task_page_data = response.context['task']
        self.assertEqual(task.name, task_page_data.name)
        self.assertEqual(task.description, task_page_data.description)
        self.assertEqual(task.status, task_page_data.status)
        self.assertEqual(task.author, task_page_data.author)
        self.assertEqual(task.executor, task_page_data.executor)
        self.assertEqual(task.labels, task_page_data.labels)

    def test_create_task(self):
        # GET page
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 200)
        # Create task
        response = self.client.post(reverse('tasks:create_task'), self.new_data, follow=True)
        self.assertRedirects(response, reverse('tasks:tasks'))
        new_task = Task.objects.last()
        self.assertTask(new_task, self.new_data)
        label_data = Label.objects.get(pk=self.new_data['labels'][0])
        self.assertContains(response, label_data)

    def test_update_task(self):
        task = Task.objects.last()
        # GET page
        response = self.client.get(reverse('tasks:update_task', kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code, 200)
        # Update task
        response = self.client.post(
            reverse('tasks:update_task', kwargs={'pk': task.pk}),
            self.update_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks:tasks'))
        updated_task = Task.objects.last()
        self.assertTask(updated_task, self.update_data)
        label_data = Label.objects.get(pk=self.update_data['labels'][0])
        self.assertContains(response, label_data)

    def test_user_delete_own_task(self):
        # GET page
        response = self.client.get(reverse('tasks:delete_task', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        # Delete task
        response = self.client.post(reverse('tasks:delete_task', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('tasks:tasks'))
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=1)

    def test_user_delete_task_from_different_author(self):
        # Attempt to GET delete task page of other author
        response = self.client.get(reverse('tasks:delete_task', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)

    def test_filter_task(self):
        query_string = '/tasks/?status=2&executor=2&label='
        response = self.client.get(query_string)
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.filter(status=2).filter(executor=2)
        self.assertQuerysetEqual(
            response.context['taskslist'],
            tasks,
            ordered=False
        )

    def test_filter_own_task(self):
        user = CustomUser.objects.get(pk=4)
        self.client.force_login(user)
        query_string = '/tasks/?status=&executor=&label=&self_tasks=on'
        response = self.client.get(query_string)
        self.assertEqual(response.status_code, 200)

        tasks = Task.objects.filter(author=user.pk)
        self.assertQuerysetEqual(
            response.context['taskslist'],
            tasks,
            ordered=False
        )
