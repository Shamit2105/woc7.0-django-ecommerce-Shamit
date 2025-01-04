from django.urls import path
from .views import ItemListView,ItemDetailView

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product_detail'),

]