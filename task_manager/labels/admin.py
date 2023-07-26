from django.contrib import admin
from task_manager.labels.models import Label


class LabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Label, LabelAdmin)
