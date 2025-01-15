from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from orders.models import UserOrder
from .forms import ItemForm, ReviewForm
from .models import Category, SubCategory, Item, Review

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self,form):
        category_name = form.cleaned_data['category_name']
        subcategories_names = form.cleaned_data.get('subcategories_name','')
        
        category, created = Category.objects.get_or_create(name=category_name)
        form.instance.category = category
        response = super().form_valid(form)
        if subcategories_names:
            subcategory_names_list = [name.strip() for name in subcategories_names.split(',')]
            for subcategory_name in subcategory_names_list:
                subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name, category=category)
                form.instance.subcategories.add(subcategory)

        return response

class ItemListView(ListView):
    template_name = 'home.html'
    context_object_name = 'items'
    def get_queryset(self):
        return Item.objects.all()
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all reviews for the specific item
        context['reviews'] = Review.objects.filter(item=self.object).order_by('-created_at')  
        return context

class SearchResultsListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return Item.objects.none()  

        items = Item.objects.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query) | 
            Q(subcategories__subcategories__icontains=query)
        ).distinct()

        if not items.exists():
            messages.warning(self.request, "No such item found.")
            return Item.objects.none()  

        return items

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return redirect('home')  
        return super().get(request, *args, **kwargs)

class ReviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        return render(request, 'review_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        if not UserOrder.objects.filter(ordered_by=request.user, item_ordered=item).exists():
            messages.error(request, "You can only review items you have purchased.")
            return redirect('userorder_list.html') 
        form = ReviewForm(request.POST)
        if form.is_valid():
            if Review.objects.filter(item=item, review_author=request.user).exists():
                messages.error(request, "You have already reviewed this item.")
                return redirect('home')
            Review.objects.create(
                item=item,
                review_author=request.user,
                review=form.cleaned_data['review'],
                rating=form.cleaned_data['rating']
            )
            messages.success(request, f"Your review for {item.name} has been successfully submitted!")
            return redirect('home')

        return render(request, 'review_form.html', {'form': form})

    