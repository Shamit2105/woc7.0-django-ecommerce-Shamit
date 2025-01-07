from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategories = models.CharField(max_length=100)

    def __str__(self):
        return self.subcategories

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.PositiveBigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.PositiveBigIntegerField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='items/')
    brand = models.CharField(max_length=100)
    subcategories = models.ManyToManyField(SubCategory)

    def discounted_price(self):
        return self.price - self.discount * self.price / 100

    def __str__(self):
        return self.name

@receiver(post_save, sender=Item)
def update_subcategories(sender, instance, **kwargs):
    for subcategory in instance.subcategories.all():
        subcategory_instance = SubCategory.objects.get(id=subcategory.id)
        subcategory_instance.save()