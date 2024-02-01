# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('chat_id', 'full_name', 'is_admin', 'is_active', 'creation')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('chat_id', 'full_name')
    ordering = ('-creation',)

    fieldsets = (
        (None, {'fields': ('chat_id', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    search_fields = ['chat_id', 'full_name']
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('chat_id', 'full_name', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )

admin.site.register(User, CustomUserAdmin)



# from django.contrib import admin
# from django.contrib.auth.models import Group
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from accounts.forms import UserCreationForm, UserchangeForm
# from accounts.models import User


# class UserAdmin(BaseUserAdmin):
#     form = UserchangeForm
#     add_form = UserCreationForm
#     list_display = ['email' , 'phone_number' , 'is_admin']
#     list_filter = ('is_admin',)
#     readonly_fields = ('last_login' , )
#     fieldsets = (
#         (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
#         ('permission', {'fields': ('is_active', 'is_admin', 'last_login', 'groups', 'user_permissions', 'is_superuser')}),
#     )

#     add_fieldsets = (
#         (None,{'fields': ('phone_number','email','full_name','password1','password2')}),
#     )

#     search_fields = ['email', 'full_name']
#     ordering = ('full_name',)
#     filter_horizontal = ('groups', 'user_permissions')

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request,obj,**kwargs)
#         is_superuser=request.user.is_superuser
#         if not is_superuser:
#             form.base_fields['is_superuer'].disabled = True
#         return form


# admin.site.register(User, UserAdmin)
