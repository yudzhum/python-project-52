from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(queryset=Status.objects.all(), label=_('Status'))
    executor = ModelChoiceFilter(queryset=CustomUser.objects.all(), label=_('Executor'))
    labels = ModelChoiceFilter(queryset=Label.objects.all(), label=_('Label'))
    self_tasks = BooleanFilter(
        field_name='self_tasks',
        method='author_of_tasks',
        label=_('Own tasks only'),
        widget=CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def author_of_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            queryset = queryset.filter(author=user)
        return queryset
