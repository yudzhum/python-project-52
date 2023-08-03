from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import ProtectedError

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import CustomLoginRequiredMixin


class ShowLabels(CustomLoginRequiredMixin, ListView):
    """Show all labels"""
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    allow_empty = True


class CreateLabel(CustomLoginRequiredMixin,
                  SuccessMessageMixin,
                  CreateView):
    """Create new label"""
    model = Label
    template_name = 'form.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label successfully created')
    extra_context = {
        'title': _('Create label'),
        'button_value': _('Create')
    }


class UpdateLabel(CustomLoginRequiredMixin,
                  SuccessMessageMixin,
                  UpdateView):
    """Update label"""
    model = Label
    template_name = 'form.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label successfully updated')
    extra_context = {
        'title': _('Edit label'),
        'button_value': _('Update')
    }


class DeleteLabel(CustomLoginRequiredMixin,
                  DeleteView):
    """Delete label"""
    model = Label
    template_name = 'delete_confirmation_form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label successfully deleted')
    extra_context = {
        'title': _('Delete label'),
    }
    deletion_denied_message = _('Cant delete label because it is in use')

    # Can't delete label because it's in use
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(
                self.request,
                messages.ERROR,
                self.deletion_denied_message
            )
        else:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                self.success_message
            )
        return HttpResponseRedirect(success_url)
