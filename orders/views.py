from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic import DetailView,ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms
from django.conf import settings
from django.core.mail import send_mail


from products.models import Item
from .forms import OrderForm
from .models import UserOrder,Order,Cart
from .mixins import CustomerRequiredMixin



class OrderConfirmView(CustomerRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        items = Order.objects.filter(user=request.user) #pela je order now ma nakhyu hoy pan order na karine kyak bije redirect kairu hoy to e item cart ma java devani
        for i in items:
            cart_item,created = Cart.objects.get_or_create(user=request.user, item=i.item)
            if not created:
                cart_item.quantity += 1
            else:
                cart_item.quantity = 1
            cart_item.save()
            i.delete()
        order, created = Order.objects.get_or_create(user=request.user, item=item)
        
        order.quantity = 1
        order.save()
        
        messages.success(request, f'{item.name} has been added to your order.')
        return redirect('order')
    
 
class OrderLView(LoginRequiredMixin,ListView):
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
        total_price = sum(item.get_total_price() for item in context['cart_items']) # to show total_price in template
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
                messages.error(request, "No Items Ordered!")
                return redirect('cart')
            for cart_item in items:
                item = cart_item.item
                quantity = cart_item.quantity
                price = item.discounted_price * quantity
                couponcode = form.cleaned_data['couponcode']
                if couponcode == 'first5':
                    discount_percentage = 5
                    price -= price * discount_percentage / 100
                    messages.success(request, f"Coupon applied! {discount_percentage}% discount on {item.name}.")
                UserOrder.objects.create(
                    ordered_by = request.user,
                    item_ordered = item,
                    quantity=quantity,
                    state = form.cleaned_data['state'],
                    city = form.cleaned_data['city'],
                    pincode = form.cleaned_data['pincode'],
                    address = form.cleaned_data['address'],
                    phone = form.cleaned_data['phone'],
                    price = price,
                    couponcode = form.cleaned_data['couponcode']
                )

                item.stock -= quantity
                item.save()
            seller_email = item.seller.email 
            subject = 'New Order Received'
            message = f'You have received a new order from {request.user.email}.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [seller_email])

            items.delete()
            messages.success(request, "Item has been ordered.")
            return redirect('my_orders')
        return render(request, 'order_form.html', {'form': form})
    
    def clean(self):
        cleaned_data = super().clean()
        user = self.user
        cart_items = UserOrder.objects.filter(user=user)
        couponcode = cleaned_data.get('couponcode')
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
                    price = item.discounted_price * quantity
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
    
class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(UserOrder, id=order_id, ordered_by=request.user)
        
        if order.can_be_canceled():
            seller_email = order.item_ordered.seller.email
            subject = 'Order Canceled'
            message = f'The order for {order.item_ordered.name} by {request.user.email} has been canceled.'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [seller_email])
            
            order.delete()
            messages.success(request, "Order has been canceled.")
        else:
            messages.error(request, "Order cannot be canceled as it is too close to the delivery date.")
        
        return redirect('my_orders')

