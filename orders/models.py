from django.db import models
from users.models import CustomUser
from products.models import Item
from datetime import timedelta,timezone

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
        return self.quantity * self.item_ordered.price
    def get_total_price(self):
        return self.quantity * self.price

    def get_delivery_date(self):
        return self.date + timedelta(days=7)  # Assuming a fixed delivery time of 7 days

 

    def get_unique_bill_id(self):
        return f'BILL-{self.id:08d}'
    

class Cart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)

    def not_in_stock(self):
        if self.quantity > self.item.stock:
            self.in_stock = False
            self.save()
        return self.in_stock
    
    def __str__(self):
        return f'{self.quantity} {self.item}'
