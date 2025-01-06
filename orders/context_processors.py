from django.db import models
from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        total_quantity = Cart.objects.filter(user=request.user).aggregate(total=models.Sum('quantity'))['total'] or 0
        return {'cart_item_count': total_quantity}
    return {'cart_item_count': 0}