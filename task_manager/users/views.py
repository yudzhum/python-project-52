from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from task_manager.users.forms import RegistrationForm, UserUpdateForm
from task_manager.users.models import CustomUser
from task_manager.users.mixins import CustomLoginRequiredMixin, PermCheckMixin


class UsersList(ListView):
    """Show users on page users"""
    model = CustomUser
    template_name = 'users/userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()


class RegisterUser(SuccessMessageMixin, CreateView):
    """Create new user"""
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'User successfully registered!'

  
class UpdateUser(CustomLoginRequiredMixin, PermCheckMixin, SuccessMessageMixin, UpdateView):
    """Change user"""
    login_url = '/login/'
    login_required_message = 'You are not authorized! Please, log in.'

    model = CustomUser
    template_name = 'users/update_user.html'
    form_class = UserUpdateForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')
    success_message = 'You profile been updated!'

    my_perm_denied_url_string = 'users:users'
    permission_denied_message = "You have no permission to change other user"


class DeleteUser(CustomLoginRequiredMixin, PermCheckMixin, SuccessMessageMixin, DeleteView):
    """Delete user"""
    login_url = '/login/'
    login_required_message = 'You are not authorized! Please, log in.'
    model = CustomUser
    template_name = 'users/delete_user.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')
    success_message = 'User was deleted'

    my_perm_denied_url_string = 'users:users'
    permission_denied_message = "You cant delete other user."

