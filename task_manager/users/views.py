from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from task_manager.users.forms import RegistrationForm, UserUpdateForm
from task_manager.users.models import CustomUser


class UsersList(ListView):
    """Show users on page users"""
    model = CustomUser
    template_name = 'users/userlist.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return CustomUser.objects.all()


class RegisterUser(CreateView):
    """Create new user"""
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    
class UpdateUser(UpdateView):
    """Change user"""
    model = CustomUser
    template_name = 'users/update_user.html'
    form_class = UserUpdateForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')


class DeleteUser(DeleteView):
    """Delete user"""
    model = CustomUser
    template_name = 'users/delete_user.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('users:users')
