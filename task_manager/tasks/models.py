from django.db import models

from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        null=False,
        related_name='author'
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='executor'
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelationModel',
        through_fields=('task', 'label'),
        blank=True,
        default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabelRelationModel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
