from django_filters import FilterSet, ModelChoiceFilter
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all())
    executor = ModelChoiceFilter(queryset=CustomUser.objects.all())
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

