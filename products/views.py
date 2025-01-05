from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView
from django.views.generic.edit import CreateView,FormView

from .models import Category, SubCategory, Item
from .forms import CategoryForm,SubCategoryForm,ItemForm
# Create your views here.

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_create.html'
    form_class = CategoryForm
    success_url = reverse_lazy('home')

class SubcategoryCreateView(CreateView):
    model = SubCategory
    template_name = 'subcategory_create.html'
    form_class = SubCategoryForm
    success_url = reverse_lazy('home')

class ItemCreateView(CreateView):
    model = Item
    template_name = 'item_create.html'
    form_class = ItemForm
    success_url = reverse_lazy('home')

class ItemListView(ListView):
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        return Item.objects.all()
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'
    
    

