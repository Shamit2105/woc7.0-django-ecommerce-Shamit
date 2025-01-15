from django.contrib import admin

#from .forms import CategoryForm, SubCategoryForm, ItemForm
from .models import Category, SubCategory, Item, Review



class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('review_author','item','rating','created_at','review')
admin.site.register(Review,ReviewAdmin)

