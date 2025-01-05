from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from .forms import UserOrderForm
from .models import UserOrder
from products.models import Item
from .mixins import CustomerRequiredMixin

class UserOrderCreateView(CustomerRequiredMixin, CreateView):
    model = UserOrder
    form_class = UserOrderForm
    template_name = 'userorder_form.html'
    success_url = reverse_lazy('home')
    
    def get_initial(self):
        initial = super().get_initial()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        initial['item_ordered'] = item
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        kwargs['item'] = item
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        form.instance.item_ordered = item
        form.instance.ordered_by = self.request.user  # Set the ordered_by field to the current user
        return super().form_valid(form)