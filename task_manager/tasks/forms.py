from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'label': _('Labels')
        }
