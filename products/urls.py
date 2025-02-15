from django.urls import path

from .views import (ItemCreateView, SellerOrderListView,SellerOrderDetailView,
                    ItemListView,ItemDetailView,ReviewView,SellerItemListView,SellerItemUpdateView)


urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product_detail'),
    path('review/<int:item_id>/', ReviewView.as_view(), name='review_form'),
    path('create_item/<int:user_id>/',ItemCreateView.as_view(),name='create_item'),
    path('seller/orders/', SellerOrderListView.as_view(), name='seller_order_list'),
    path('seller/items/',SellerItemListView.as_view(),name='seller_item_list'),
    path('seller/orders/<int:order_id>/', SellerOrderDetailView.as_view(), name='seller_order_detail'),
    path("seller_item_update/<int:item_id>/", SellerItemUpdateView.as_view(), name="seller_item_update"),
    #path('searchresults/',SearchResultsListView.as_view(),name='search_results')
]
