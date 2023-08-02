from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    """Home page"""
    template_name = "index.html"


class LoginUserView(SuccessMessageMixin, LoginView):
    """Login user"""
    template_name = 'form.html'
    form_class = AuthenticationForm
    success_message = _('You have successfully logged in')
    extra_context = {
        'title': _('Login'),
        'button_value': _('Log in')
    }

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    """Logout user"""

    def get_success_url(self):
        success_url = reverse_lazy('home')
        messages.add_message(
            self.request,
            messages.INFO,
            _('You have successfully logged out!')
        )
        return success_url
