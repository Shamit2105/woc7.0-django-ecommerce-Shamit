from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms

from products.models import Item
from .forms import UserOrderForm,OrderForm
from .models import UserOrder,Order,Cart
from .mixins import CustomerRequiredMixin



class OrderConfirmView(View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        items = Order.objects.filter(user=request.user)
        for i in items:
            i.delete()
        order, created = Order.objects.get_or_create(user=request.user, item=item)
        if created:
            order.quantity = 1
        else:
            order.quantity = 1
        order.save()
        
        messages.success(request, f'{item.name} has been added to your order.')
        return redirect('order')
    
 
class OrderLView(ListView):
    model = Order
    template_name = 'order_summary.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        # Fetch current orders
        orders = Order.objects.filter(user=self.request.user)
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate total price of current orders
        total_price = sum(item.get_total_price() for item in context['cart_items'])
        context['total_price'] = total_price
        
        return context

class OrderIncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Order, id=kwargs['pk'], user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('order')

class OrderDecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Order, id=kwargs['pk'], user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('order')

class OrderView(View): #will have to use view instead of createview as items bulk ma 
    def get(self,request,*args,**kwargs):
        form = OrderForm
        return render(request, 'order_form.html', {'form': form})

    def post(self,request,*args,**kwargs):
        form = OrderForm(request.POST)
        
        if form.is_valid():
            items = Order.objects.filter(user=request.user)
            if not items.exists():
                messages.error(request, "Your cart is empty.")
                return redirect('cart')
            for cart_item in items:
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
            items.delete()
            messages.success(request, "All items in your cart have been ordered.")
            return redirect('my_orders')
        return render(request, 'order_form.html', {'form': form})
    
    def clean(self):
        cleaned_data = super().clean()
        user = self.user
        cart_items = Order.objects.filter(user=user)
        for cart_item in cart_items:
            item = cart_item.item
            if cart_item.quantity > item.stock:
                messages.error( "No stock available")
                redirect('home')
        return cleaned_data

class UserOrderBillView(LoginRequiredMixin,DetailView):
    model = UserOrder
    template_name = 'userorder_bill.html'
    context_object_name = 'order'

class PreviousOrderListView(LoginRequiredMixin, ListView):
    model = UserOrder
    template_name = 'userorder_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return UserOrder.objects.filter(ordered_by=self.request.user).order_by('-date')
    
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        cart_item,created = Cart.objects.get_or_create(user=request.user, item=item)
        if not created:
            cart_item.quantity += 1
        else:
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
    
class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'], user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')

class DecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item = get_object_or_404(Cart, id=kwargs['pk'], user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    
class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
class CartOrderView(View): #will have to use view instead of createview as items bulk ma 
    def get(self,request,*args,**kwargs):
        form = OrderForm
        return render(request, 'cart_order.html', {'form': form})

    def post(self,request,*args,**kwargs):
        form = OrderForm(request.POST)
        
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

