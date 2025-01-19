from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,View,UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from users.models import CustomUser
from orders.models import UserOrder
from .forms import ItemForm, ReviewForm
from .models import Category, SubCategory, Item, Review

class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item_create.html'
    success_url = reverse_lazy('home')

class ItemListView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # Handle initial page load or reset filters
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        items = Item.objects.all()

        return render(request, self.template_name, {
            'categories': categories,
            'subcategories': subcategories,
            'items': items,
        })

    def post(self, request, *args, **kwargs):
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        items = Item.objects.all()
        if category:
            items = items.filter(category__name=category)
        if subcategory:
            items = items.filter(subcategories__name=subcategory)
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        return render(request, self.template_name, {
            'categories': categories,
            'subcategories': subcategories,
            'items': items,
            'selected_category': category,
            'selected_subcategory': subcategory,
        })

    
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
            Q(subcategories__name__icontains=query)
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

class SellerItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = "seller_item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_queryset()
        return context

class SellerItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'seller_item_update.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        item_id = self.kwargs.get("item_id")
        return Item.objects.get(id=item_id)

class SellerOrderListView(LoginRequiredMixin, ListView):
    template_name = 'seller_order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return UserOrder.objects.filter(item_ordered__seller=self.request.user).select_related('item_ordered', 'ordered_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.get_queryset()
        return context


class SellerOrderDetailView(LoginRequiredMixin, View):
    template_name = "seller_order.html"

    def get(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        order = get_object_or_404(UserOrder, id=order_id)

        if order.item_ordered.seller != self.request.user:
            messages.warning(request, "You can only access orders for items you are selling.")
            return redirect('seller_order_list')

        context = {
            'customer': order.ordered_by,
            'quantity': order.quantity,
            'state': order.state,
            'city': order.city,
            'pin': order.pincode,
            'address': order.address,
            'phno': order.phone,
            'billno': order.get_unique_bill_id,
            'date': order.date,
            'item': order.item_ordered,
        }
        return render(request, self.template_name, context)



    
        
        
        
        
     
