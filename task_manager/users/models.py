from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """User model"""

    def __str__(self):
        return self.get_full_name()
