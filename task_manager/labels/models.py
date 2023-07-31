from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
