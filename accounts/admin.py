from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['full_name', 'email', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['full_name', 'email']

    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']


admin.site.register(User, UserAdmin)
