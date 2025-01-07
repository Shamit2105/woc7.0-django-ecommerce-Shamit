from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView,FormView
from django.views import View
from django.contrib.auth.hashers import make_password

from .forms import CustomUserCreationForm, PasswordResetRequestForm,PasswordResetForm,PasswordChangeForm
from .models import CustomUser

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class PasswordResetRequestView(FormView):
    form_class = PasswordResetRequestForm
    template_name = 'registration/password_reset_request.html'
    success_url = reverse_lazy('password_reset_request')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        security_question = form.cleaned_data['security_question']
        security_answer = form.cleaned_data['security_answer']

        try:
            user = CustomUser.objects.get(email=email)
            if user.security_question != security_question:
                form.add_error('security_question', 'Incorrect security question.')
            else:
                if user.security_answer == security_answer:
                    return redirect('password_reset_form', user_id=user.id)
                else:
                    form.add_error('security_answer', 'Incorrect security answer.')
        except CustomUser.DoesNotExist:
            form.add_error('email', 'Email not found.')
        return self.form_invalid(form)

class PasswordResetFormView(FormView):
    form_class = PasswordResetForm
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        new_password = form.cleaned_data['new_password']
        user = CustomUser.objects.get(id=user_id)
        user.password = make_password(new_password)
        user.save()
        return super().form_valid(form)
    
class PasswordChangeView(FormView):
    form_class = PasswordChangeForm
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']
        confirm_password = form.cleaned_data['confirm_password']
        user = self.request.user
        if user.check_password(old_password):
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.save()
                return super().form_valid(form)
            else:
                form.add_error('confirm_password', 'Passwords do not match.')
        else:
            form.add_error('old_password', 'Incorrect password.')
        return self.form_invalid(form)

    


