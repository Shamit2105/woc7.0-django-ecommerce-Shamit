from django.db import models
from users.models import CustomUser
from products.models import Item
from datetime import timedelta

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
        return self.quantity * self.item_ordered.discounted_price()
    

    def get_delivery_date(self):
        delivery_date = self.date + timedelta(days=7)  # Assuming a fixed delivery time of 7 days
        return f'by {delivery_date.strftime("%d-%m-%Y %H:%M:%S")}'
 

    def get_unique_bill_id(self):
        return f'BILL-{self.id:08d}'
    

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.item.discounted_price() * self.quantity
    
    def __str__(self):
        return f'{self.user.username} - {self.item.name} - '


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.item.discounted_price() * self.quantity
    
    def __str__(self):
        return f'{self.user.username} - {self.item.name} - '
