from django.db import models
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=False)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False, related_name='author')
    executor = models.ForeignKey(CustomUser,  on_delete=models.PROTECT, blank=True, default='', related_name='executor')
    # change after label model creation
    label = models.CharField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
