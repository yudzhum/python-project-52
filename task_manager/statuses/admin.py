from django.contrib import admin
from task_manager.statuses.models import Status


class StatusAdmin(admin.ModelAdmin):
    pass


admin.site.register(Status, StatusAdmin)
