from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


from products.models import Item
from .forms import UserOrderForm
from .models import UserOrder,Cart
from .mixins import CustomerRequiredMixin

class UserOrderCreateView(CustomerRequiredMixin, CreateView):
    model = UserOrder
    form_class = UserOrderForm
    template_name = 'userorder_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        initial['item_ordered'] = item
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        kwargs['item'] = item
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        form.instance.item_ordered = item
        form.instance.ordered_by = self.request.user  
        form.save()  
        return redirect('order_bill', pk=form.instance.pk)

class UserOrderBillView(LoginRequiredMixin,DetailView):
    model = UserOrder
    template_name = 'userorder_bill.html'
    context_object_name = 'order'

class UserOrderListView(LoginRequiredMixin, ListView):
    model = UserOrder
    template_name = 'userorder_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return UserOrder.objects.filter(ordered_by=self.request.user).order_by('-date')
    
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('home')
    
class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'cart_list.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_price = sum(item.get_total_price() for item in context['cart_items'])
        context['total_price'] = total_price
        return context
    

