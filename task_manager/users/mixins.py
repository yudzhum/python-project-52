from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login


class CustomLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated"""

    # Default url and message. Can be overriden in view.
    login_url = '/login/'
    # This message does not translate automatically.
    # Add translation in view.
    login_required_message = 'You are not authorized! Please, log in.'

    def get_login_url(self) -> str:
        login_url = self.login_url
        messages.add_message(
            self.request,
            messages.ERROR,
            self.login_required_message
        )
        return login_url

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name()
            )
        return super().dispatch(request, *args, **kwargs)


class CustomUserPassesTestMixin(AccessMixin):
    """
    Deny a request and show error message if user not themself.
    Differs from the basic one in django, by possibility
    to add a message and link to redirect,
    the default one shows a 403 error.
    """
    my_perm_denied_url_string = 'users:users'
    permission_denied_message = ""

    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, self.permission_denied_message)
        return redirect(reverse_lazy(self.my_perm_denied_url_string))

    # Default test
    # Comparing object pk with user.pk
    # Can be overriden in view.
    def test_func(self):
        obj = self.get_object()
        return obj.pk == self.request.user.pk

    def get_test_func(self):
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
