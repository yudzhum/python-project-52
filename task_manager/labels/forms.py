from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name')
        }
