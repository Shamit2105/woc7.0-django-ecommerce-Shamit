from django.contrib import admin

from .forms import UserOrderForm
from .models import UserOrder, Cart

class UserOrderAdmin(admin.ModelAdmin):
    add_form = UserOrderForm
    model = UserOrder
    list_display = ['ordered_by', 'item_ordered', 'quantity', 'price','state', 'city', 'pincode', 'address', 'phone', 'date', 'couponcode']
admin.site.register(UserOrder, UserOrderAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['user','item', ]
admin.site.register(Cart, CartOrderAdmin)