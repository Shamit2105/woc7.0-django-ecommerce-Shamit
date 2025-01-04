from django import forms

from .models import UserOrder, Cart

class UserOrderForm(forms.ModelForm):
    class Meta:
        model = UserOrder
        fields = ['quantity', 'state', 'city', 'pincode', 'address', 'phone', 'couponcode']



class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']