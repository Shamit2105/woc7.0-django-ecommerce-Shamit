from django.shortcuts import render
from django.views.generic import ListView,TemplateView,DetailView

from .models import Category, SubCategory, Item
# Create your views here.

class ItemListView(ListView):
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        return Item.objects.all()
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'
    
    

