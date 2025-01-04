from django import forms

from .models import UserOrder, Cart
from products.models import Item

class UserOrderForm(forms.ModelForm):
    

    class Meta:
        model = UserOrder
        fields = [ 'quantity', 'state', 'city', 'pincode', 'address', 'phone', 'couponcode']
    def save(self, commit=True):
        order = super().save(commit=False)
        order.item_ordered.stock -= order.quantity
        order.item_ordered.save()
        if commit:
            order.save()
        return order

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']