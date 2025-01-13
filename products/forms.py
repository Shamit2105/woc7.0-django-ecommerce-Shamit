from django import forms
from .models import Category, SubCategory, Item,Review

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'subcategories']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category', 'discount', 'stock', 'image', 'brand', 'subcategories']
        widgets = {
            'subcategories': forms.CheckboxSelectMultiple(),
        }
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review'] 
        

    