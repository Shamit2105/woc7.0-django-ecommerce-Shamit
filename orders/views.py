from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

from .forms import UserOrderForm, CartForm
from .models import UserOrder, Cart
from products.models import Item

class UserOrderCreateView(CreateView):
    model = UserOrder
    form_class = UserOrderForm
    template_name = 'userorder_form.html'
    success_url = reverse_lazy('home')
    
    def order_failed(self, form):
        item = form.cleaned_data['item_ordered']
        quantity = form.cleaned_data['quantity']
        if quantity > item.stock:
            form.add_error('quantity', 'Ordered quantity exceeds available stock.')
            return True
        return False

    def form_valid(self, form):
        if self.order_failed(form):
            return self.form_invalid(form)
        response = super().form_valid(form)
        return redirect(self.success_url)


