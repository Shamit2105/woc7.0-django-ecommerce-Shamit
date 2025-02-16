from django.db import models
from users.models import CustomUser
from products.models import Item
from datetime import timedelta,datetime
from django.utils import timezone

class UserOrder(models.Model):
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_ordered = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    phone = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    couponcode = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,null=True)

    def __str__(self):
        return f'{self.ordered_by} ordered {self.quantity} {self.item_ordered} on {self.date}'
    
    def get_total_price(self):
        price = self.quantity * self.item_ordered.discounted_price
        return price
    

    def get_delivery_date(self):
        return self.date + timedelta(days=7)

 

    def get_unique_bill_id(self):
        return f'BILL-{self.id:08d}'
    
    def can_be_canceled(self):
        current_date = timezone.now()  # Use Django's timezone-aware datetime
        delivery_date = self.get_delivery_date()
        return (delivery_date - current_date).days >= 2

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.item.discounted_price * self.quantity
    
    def __str__(self):
        return f'{self.user.username} - {self.item.name} - '


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.item.discounted_price * self.quantity
    
    def __str__(self):
        return f'{self.user.username} - {self.item.name} - '
