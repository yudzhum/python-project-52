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
        response = self.client.get(reverse('tasks:update_task', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))

    def test_delete_task_page_without_login(self):
        response = self.client.get(reverse('tasks:delete_task', kwargs={'pk': 1 }))
        self.assertEqual(response.status_code, 302)       
        self.assertTrue(response.url.startswith('/login/'))

    def test_show_task_page_without_login(self):
        response = self.client.get(reverse('tasks:show_task', kwargs={'pk': 1 }))
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
        response = self.client.get(reverse('tasks:show_task', kwargs={'pk': task.pk }))
        self.assertEqual(response.status_code, 200)
        task_on_page = response.context['task']
        self.assertEqual(task.name, task_on_page.name)
        self.assertEqual(task.description, task_on_page.description)
        self.assertEqual(task.status, task_on_page.status)
        self.assertEqual(task.author, task_on_page.author)
        self.assertEqual(task.executor, task_on_page.executor)
        self.assertEqual(task.labels, task_on_page.labels)

    def test_create_task(self):
        # GET page
        response = self.client.get(reverse('tasks:create_task'))
        self.assertEqual(response.status_code, 200)
        # Create status
        response = self.client.post(reverse('tasks:create_task'), self.new_data, follow=True)
        new_task = Task.objects.last()
        self.assertTask(new_task, self.new_data)
        label_data = Label.objects.get(pk=self.new_data['labels'][0])
        self.assertContains(response, label_data)
 

    def test_update_task(self):
        pass

    def test_user_delete_own_task(self):
        pass

    def test_user_delete_task_from_different_user(self):
        pass
