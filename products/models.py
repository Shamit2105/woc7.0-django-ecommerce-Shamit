from django.db import models
from django.db.models.signals import post_save,post_delete
from django.db.models import Avg
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
    ratings = models.DecimalField(default=0.0,max_digits=3,decimal_places=2)
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  

    def save(self, *args, **kwargs):
        self.discounted_price = self.price * (1 - self.discount / 100)
        super().save(*args, **kwargs)

    def update_avg_rating(self):
        avg = self.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
        self.avg_rating = avg if avg else 0.0
        self.save(update_fields=['avg_rating'])

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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.item.update_avg_rating()

    def delete(self, *args, **kwargs):
        item = self.item
        super().delete(*args, **kwargs)
        item.update_avg_rating()

    def __str__(self):
        return f"Review for {self.item.name} by {self.review_author.username}"



    




