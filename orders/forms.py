from django import forms
from django.core.exceptions import ValidationError

from products.models import Review
from .models import UserOrder, Cart,Order

class OrderForm(forms.Form):
    state = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=6)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=10)
    couponcode = forms.CharField(max_length=10,required=False)







    
