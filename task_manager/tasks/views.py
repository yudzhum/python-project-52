from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter
from task_manager.users.mixins import CustomLoginRequiredMixin, CustomUserPassesTestMixin
from task_manager.users.models import CustomUser


class TasksList(CustomLoginRequiredMixin, FilterView, ListView):
    """Show all tasks"""
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'taskslist'
    allow_empty = True
    filterset_class = TaskFilter
    extra_context = {
        'button_value': _('Show')
    }


class ShowTask(CustomLoginRequiredMixin, DetailView):
    """Show tasks detail"""
    model = Task
    template_name = 'tasks/show_task.html'
    context_object_name = 'task'


class CreateTask(CustomLoginRequiredMixin,
                 SuccessMessageMixin,
                 CreateView):
    """Create new task"""
    model = Task
    template_name = 'form.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully created')
    extra_context = {
        'title': _('Create task'),
        'button_value': _('Create')
    }

    def form_valid(self, form):
        user_pk = self.request.user.pk
        form.instance.author = CustomUser.objects.get(pk=user_pk)
        return super().form_valid(form)


class UpdateTask(CustomLoginRequiredMixin,
                 SuccessMessageMixin,
                 UpdateView):
    """Update task"""
    model = Task
    template_name = 'form.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully updated')
    extra_context = {
        'title': _('Edit task'),
        'button_value': _('Update')
    }


class DeleteTask(CustomLoginRequiredMixin,
                 CustomUserPassesTestMixin,
                 SuccessMessageMixin,
                 DeleteView):
    """Delete task"""
    model = Task
    template_name = 'delete_confirmation_form.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully deleted')
    extra_context = {
        'title': _('Delete task'),
    }
    my_perm_denied_url_string = 'tasks:tasks'
    permission_denied_message = _('Only author can delete task')

    # Check if user is author of task
    def test_func(self):
        task = self.get_object()
        return task.author.pk == self.request.user.pk
