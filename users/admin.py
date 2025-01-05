from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'phno', 'country', 'state', 'security_question', 'security_answer']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phno', 'country', 'state', 'security_question', 'security_answer','user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phno', 'country', 'state', 'security_question', 'security_answer','user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)