from django.urls import path
from .views import CategoryCreateView,SubcategoryCreateView,ItemCreateView,ItemListView,ItemDetailView

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product_detail'),
    path('create_category/<int:user_id>/',CategoryCreateView.as_view(),name='create_category'),
    path('create_subcategory/<int:user_id>/',SubcategoryCreateView.as_view(),name='create_subcategory'),
    path('create_item/<int:user_id>/',ItemCreateView.as_view(),name='create_item'),
]