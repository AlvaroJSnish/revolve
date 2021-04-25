from django.contrib import admin

from .models import Stat


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_type', 'project_plan', 'features_columns', 'elapsed_time', 'trained_date')
    readonly_fields = ('id',)
