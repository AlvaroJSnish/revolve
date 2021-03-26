from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    exclude = ('groups', 'user_permissions',)
    readonly_fields = ('id', 'password', 'last_login',)

    # update password
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        obj.save()
