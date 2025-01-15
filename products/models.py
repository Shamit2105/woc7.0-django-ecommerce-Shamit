from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)  # changed to field name for clarity
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        unique_together = ('name', 'category')  

    def __str__(self):
        return f"{self.name} ({self.category.name})"

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


class Review(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,default=1)
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    review_author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(choices=RATING_CHOICES,default=3)
    review = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Review for {self.item.name} by {self.review_author.username}"

@receiver(post_save, sender=Item)
def update_subcategories(sender, instance, **kwargs):
    for subcategory in instance.subcategories.all():
        subcategory_instance = SubCategory.objects.get(id=subcategory.id)
        subcategory_instance.save()