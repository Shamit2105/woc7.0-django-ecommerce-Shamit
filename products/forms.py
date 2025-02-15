from django import forms
from .models import Category, SubCategory, Item,Review

class ItemForm(forms.ModelForm):
    category_name = forms.CharField(max_length=100, required=True)
    subcategories_names = forms.CharField(max_length=500, required=False, help_text="Comma-separated list of subcategories")

    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category_name', 'discount', 'stock', 'image', 'brand', 'subcategories_names']

    def save(self, commit=True, user=None):  
        category_name = self.cleaned_data['category_name']
        subcategories_names = self.cleaned_data['subcategories_names']
        
        category, created = Category.objects.get_or_create(name=category_name)

        item = super().save(commit=False)
        item.category = category

        if user and user.is_authenticated: 
            item.seller = user

        if commit:
            item.save()

        if subcategories_names:
            subcategory_names_list = [name.strip() for name in subcategories_names.split(',')]
            for subcategory_name in subcategory_names_list:
                subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
                item.subcategories.add(subcategory)

        return item
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review'] 
        

    