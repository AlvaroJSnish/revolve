from django.contrib import admin

from .models import Project, ProjectConfiguration, ProjectConfigFile

# Register your models here.


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'owner', 'project_configuration')
    readonly_fields = ('id', 'owner',)


@admin.register(ProjectConfiguration)
class ProjectConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('id', 'project',)


@admin.register(ProjectConfigFile)
class ProjectConfigFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_configuration')
    readonly_fields = ('id', 'project_configuration')