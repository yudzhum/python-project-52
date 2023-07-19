from django.contrib import admin
from task_manager.users.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
