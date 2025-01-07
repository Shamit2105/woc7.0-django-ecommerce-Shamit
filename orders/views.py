from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms

from products.models import Item
from .forms import UserOrderForm,CartOrderForm
from .models import UserOrder,Cart
from .mixins import CustomerRequiredMixin

class UserOrderCreateView(CustomerRequiredMixin, CreateView):
    model = UserOrder
    form_class = UserOrderForm
    template_name = 'userorder_form.html'
    
    def get_initial(self):#set item_ordered to item by default when it loads
        initial = super().get_initial()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        initial['item_ordered'] = item
        return initial

    def get_form_kwargs(self):#pass the data of order for logged in user
        kwargs = super().get_form_kwargs()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        kwargs['item'] = item
        kwargs['user'] = self.request.user  
        return kwargs

    def form_valid(self, form):#check for stock-quantity inequality and 
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, pk=item_id)
        quantity = form.cleaned_data['quantity']

        if quantity > item.stock:
            messages.error(self.request, "No stock available")
            return redirect('home')
        
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
    
class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
class CartOrderView(View): #will have to use view as items bulk ma 
    def get(self,request,*args,**kwargs):
        form = CartOrderForm
        return render(request, 'cart_order.html', {'form': form})

    def post(self,request,*args,**kwargs):
        form = CartOrderForm(request.POST)
        
        if form.is_valid():
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                messages.error(request, "Your cart is empty.")
                return redirect('cart')
            for cart_item in cart_items:
                item = cart_item.item
                quantity = cart_item.quantity
                UserOrder.objects.create(
                    ordered_by = request.user,
                    item_ordered = item,
                    quantity=quantity,
                    state = form.cleaned_data['state'],
                    city = form.cleaned_data['city'],
                    pincode = form.cleaned_data['pincode'],
                    address = form.cleaned_data['address'],
                    phone = form.cleaned_data['phone'],
                    price = item.discounted_price() * quantity
                )
                item.stock -= quantity
                item.save()
            cart_items.delete()
            messages.success(request, "All items in your cart have been ordered.")
            return redirect('my_orders')
        return render(request, 'order_form.html', {'form': form})
    
    def clean(self):
        cleaned_data = super().clean()
        user = self.user
        cart_items = Cart.objects.filter(user=user)
        for cart_item in cart_items:
            item = cart_item.item
            if cart_item.quantity > item.stock:
                messages.error( "No stock available")
                redirect('home')
        return cleaned_data

