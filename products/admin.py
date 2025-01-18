from django.contrib import admin

from .forms import ItemForm
from .models import Category, SubCategory, Item, Review

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', )

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    
    list_display = ('name','category')
admin.site.register(SubCategory, SubCategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    model = Item
    add_form = ItemForm
    
    list_display = ('name', 'description', 'price', 'category', 'discount', 'stock', 'image', 'brand',)

admin.site.register(Item, ItemAdmin)


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('review_author','item','rating','created_at','review')
admin.site.register(Review,ReviewAdmin)

