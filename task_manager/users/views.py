from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import RegistrationForm, UserUpdateForm
from task_manager.users.models import CustomUser
from task_manager.users.mixins import CustomLoginRequiredMixin, CustomUserPassesTestMixin


class UsersList(ListView):
    """Show users on page users"""
    model = CustomUser
    template_name = 'users/userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()


class RegisterUser(SuccessMessageMixin, CreateView):
    """Create new user"""
    template_name = 'users/form.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered!')
    extra_context = {
        'title': _('Registration'),
        'button_value': _('Registration')
    }


class UpdateUser(CustomLoginRequiredMixin,
                 CustomUserPassesTestMixin,
                 SuccessMessageMixin,
                 UpdateView):
    """
    Change user.
    User shoud be logged in and can update only themself.
    """
    login_url = '/login/'
    login_required_message = _('You are not authorized! Please, log in.')

    model = CustomUser
    template_name = 'users/form.html'
    form_class = UserUpdateForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')
    success_message = _('You profile been updated!')
    extra_context = {
        'title': _('User update'),
        'button_value': _('Update')
    }

    my_perm_denied_url_string = 'users:users'
    permission_denied_message = _("You have no permission to change other user")


class DeleteUser(CustomLoginRequiredMixin,
                 CustomUserPassesTestMixin,
                 SuccessMessageMixin,
                 DeleteView):
    """
    Delete user.
    User shoud be logged in and can delete only themself.
    """
    login_url = '/login/'
    login_required_message = _('You are not authorized! Please, log in.')

    model = CustomUser
    template_name = 'users/delete_user.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')
    success_message = _('User was deleted')

    my_perm_denied_url_string = 'users:users'
    permission_denied_message = _("You have no permission to change other user")
