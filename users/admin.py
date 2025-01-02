from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm,UserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['username','email','first_name','last_name','phno','country','state','security_question','security_answer']

admin.site.register(CustomUser, CustomUserAdmin)
