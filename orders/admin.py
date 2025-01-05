from django.contrib import admin

from .forms import UserOrderForm,CartForm
from .models import UserOrder, Cart

class UserOrderAdmin(admin.ModelAdmin):
    add_form = UserOrderForm
    model = UserOrder
    list_display = ['ordered_by', 'item_ordered', 'quantity', 'price','state', 'city', 'pincode', 'address', 'phone', 'date', 'couponcode']
admin.site.register(UserOrder, UserOrderAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    add_form = CartForm
    model = Cart
    list_display = ['item', 'quantity', 'in_stock']
admin.site.register(Cart, CartOrderAdmin)