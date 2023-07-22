from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status


class StatusForm(ModelForm):
    name = forms.CharField(label=_('Name'))

    class Meta:
        model = Status
        fields = ['name']
