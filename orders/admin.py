from django.contrib import admin
from .models import UserOrder, Cart, Order

class UserOrderAdmin(admin.ModelAdmin):
    model = UserOrder
    list_display = ['ordered_by', 'item_ordered', 'quantity','state', 'city', 'pincode', 'address', 'phone', 'date', 'couponcode']
admin.site.register(UserOrder, UserOrderAdmin)

class CartOrderAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['user','item', ]
admin.site.register(Cart, CartOrderAdmin)

class UserOAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['user','item', 'quantity']
admin.site.register(Order,UserOAdmin)