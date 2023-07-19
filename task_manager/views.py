from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    """Home page"""
    template_name = "index.html"


class LoginUserView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    success_message = "you are logged out"

    def get_success_url(self):
        return reverse_lazy('home')
