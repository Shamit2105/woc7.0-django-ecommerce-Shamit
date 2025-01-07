from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib import messages
from .forms import CategoryForm, SubCategoryForm, ItemForm
from .models import Category, SubCategory, Item

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

    def get_form(self, form_class=None):
        form = super(ItemCreateView, self).get_form(form_class)
        form.fields['subcategories'].queryset = SubCategory.objects.none()

        if self.request.POST:
            form = ItemForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                category_id = form.cleaned_data.get('category').id
                form.fields['subcategories'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('subcategories')
        else:
            form = ItemForm()
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        subcategories = form.cleaned_data['subcategories']
        for subcategory in subcategories:
            self.object.subcategories.add(subcategory)
        messages.success(self.request, "Item created successfully.")
        return response

class ItemListView(ListView):
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        return Item.objects.all()
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'