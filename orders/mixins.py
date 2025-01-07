from django.shortcuts import redirect
from django.contrib import messages

class CustomerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'customer':
            messages.error(request, "Please login as a customer.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)