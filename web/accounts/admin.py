# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('chat_id', 'full_name', 'is_admin', 'is_active','is_superuser', 'creation')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('chat_id', 'full_name')
    ordering = ('-creation',)

    fieldsets = (
        (None, {'fields': ('chat_id', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active','is_superuser')}),
    )

    search_fields = ['chat_id', 'full_name']
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('chat_id', 'full_name', 'password1', 'password2', 'is_admin', 'is_active' , 'is_superuser',),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if obj and obj.is_admin:
            return super().get_fieldsets(request, obj) + (('Permissions', {'fields': ( 'user_permissions',)}),)
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj and not obj.is_admin:
            return super().get_readonly_fields(request, obj) + ( 'user_permissions',)
        return super().get_readonly_fields(request, obj)

admin.site.register(User, CustomUserAdmin)
