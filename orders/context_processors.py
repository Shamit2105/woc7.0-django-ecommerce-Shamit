from django.db import models
from .models import Cart,UserOrder

def cart_item_count(request):
    if request.user.is_authenticated and request.user.user_type=='customer':
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total=models.Sum('quantity'))['total'] or 0
        return {'cart_item_count': total_quantity}
    return {'cart_item_count': 0}

