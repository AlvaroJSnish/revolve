from django.contrib import admin

from .models import UserStats, ProjectVisits


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'regression_models_trained', 'classification_models_trained', 'average_accuracy',
                    'average_accuracy')
    readonly_fields = ('id', 'user',)


@admin.register(ProjectVisits)
class ProjectVisitsAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'visits')
    readonly_fields = ('id', 'project',)
