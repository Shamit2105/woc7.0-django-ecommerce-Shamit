from django.db import models
from django.db.models.signals import post_save,post_delete
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

    """ jyare aapni entity(item) bija entity ni foreign key hoy ane e entity ni item specific fields access
    karvi hoy tyare e class name_set.all() karine kari saki"""
    def avg_rating(self): 
        reviews = self.review_set.all()
        if reviews:
            total = sum(review.rating for review in reviews)
            avg = total/reviews.count()
            return avg
        return 0.0
        

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
    



