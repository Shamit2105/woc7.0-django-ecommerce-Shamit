from django.contrib import admin

from .forms import CategoryForm, SubCategoryForm, ItemForm
from .models import Category, SubCategory, Item

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    add_form = CategoryForm
    list_display = ('name', 'description')

admin.site.register(Category, CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    add_form = SubCategoryForm
    list_display = ('subcategories',)
admin.site.register(SubCategory, SubCategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    model = Item
    add_form = ItemForm
    list_display = ('name', 'description', 'price', 'category', 'discount', 'stock', 'image', 'brand')
admin.site.register(Item, ItemAdmin)

