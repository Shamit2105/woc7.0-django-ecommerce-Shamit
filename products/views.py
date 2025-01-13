from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from orders.models import UserOrder
from .forms import CategoryForm, SubCategoryForm, ItemForm, ReviewForm
from .models import Category, SubCategory, Item, Review

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

    def get_form(self, form_class=None):#to display subcategories option that the seller currently has
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

    def form_valid(self, form):#after validating form, we add subcategory to subcategories
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all reviews for the specific item
        context['reviews'] = Review.objects.filter(item=self.object).order_by('-created_at')  # Assuming `created_at` exists
        return context

class SearchResultsListView(ListView):
    model = Item
    context_object_name = 'items'
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            return Item.objects.none()  # Return an empty queryset if no query is provided

        items = Item.objects.filter(
            Q(name__icontains=query) | 
            Q(category__name__icontains=query) | 
            Q(subcategories__subcategories__icontains=query)
        ).distinct()

        if not items.exists():
            messages.warning(self.request, "No such item found.")
            return Item.objects.none()  # Return an empty queryset to prevent errors

        return items

    def get(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return redirect('home')  # Redirect to home if no items are found
        return super().get(request, *args, **kwargs)

class ReviewView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        return render(request, 'review_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)

        # Check if the user has ordered this item
        if not UserOrder.objects.filter(ordered_by=request.user, item_ordered=item).exists():
            messages.error(request, "You can only review items you have purchased.")
            return redirect('userorder_list.html')  # Redirect to item detail or another page

        # Process the review form
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

        # Re-render form on error
        return render(request, 'review_form.html', {'form': form})

    