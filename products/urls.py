from django.urls import path
from .views import (ItemCreateView,
                    ItemListView,ItemDetailView,SearchResultsListView,ReviewView,SellerItemListView)

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product_detail'),
    path('review/<int:item_id>/', ReviewView.as_view(), name='review_form'),
    path('create_item/<int:user_id>/',ItemCreateView.as_view(),name='create_item'),
    path('seller_list/<int:user_id>',SellerItemListView.as_view(),name='seller_list'),
    path('searchresults/',SearchResultsListView.as_view(),name='search_results')
]
