from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class ShowStatuses(ListView):
    """Show all statuses"""
    model = Status
    template_name = 'statuses/statuses_index.html'
    context_object_name = 'statuses'
    allow_empty = True

    def get_queryset(self):
        return Status.objects.all()


class CreateStatus(SuccessMessageMixin, CreateView):
    """Create new status"""
    template_name = 'form.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_value': _('Create')
    }


class UpdateStatus(SuccessMessageMixin, UpdateView):
    """Update status"""
    template_name = 'form.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status successfully updated')
    extra_context = {
        'title': _('Edit status'),
        'button_value': _('Update')
    }


class DeleteStatus(SuccessMessageMixin, DeleteView):
    """Delete status"""
    template_name = 'delete_confirmation_form.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status successfully deleted')
    extra_context = {
        'title': _('Delete status'),
    }
