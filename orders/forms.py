from django import forms
from django.core.exceptions import ValidationError
from .models import UserOrder, Cart

class UserOrderForm(forms.ModelForm):
    price = forms.CharField(label='Price', required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = UserOrder
        fields = ['quantity', 'state', 'city', 'pincode', 'address', 'phone', 'couponcode', 'price']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)
        if item:
            self.fields['price'].initial = item.discounted_price()


    def save(self, commit=True):
        order = super().save(commit=False)
        order.item_ordered.stock -= order.quantity
        order.item_ordered.save()
        order.price = order.item_ordered.discounted_price() * order.quantity
        if commit:
            order.save()
        return order

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']