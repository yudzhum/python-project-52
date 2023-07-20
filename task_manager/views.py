from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy


class IndexView(TemplateView):
    """Home page"""
    template_name = "index.html"


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_message = 'You have successfully logged in'

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    
    def get_success_url(self):
        success_url = reverse_lazy('home')
        messages.add_message(
        self.request, messages.SUCCESS,
        'You have successfully logged out!'
        )
        return success_url
