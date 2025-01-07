from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name', 'phno', 'country', 'state', 'security_question', 'security_answer','user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=100)
    security_question = forms.ChoiceField(choices=[])
    security_answer = forms.CharField(max_length=100, widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['security_question'].choices = CustomUser.questions
    

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    