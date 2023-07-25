from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.mixins import CustomLoginRequiredMixin


class ShowLabels(CustomLoginRequiredMixin, ListView):
    """Show all statuses"""
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'
    allow_empty = True


class CreateLabel(CustomLoginRequiredMixin,
                   SuccessMessageMixin,
                   CreateView):
    """Create new status"""
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
    """Update status"""
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
                   SuccessMessageMixin,
                   DeleteView):
    """Delete status"""
    model = Label
    template_name = 'delete_confirmation_form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label successfully deleted')
    extra_context = {
        'title': _('Delete label'),
    }
