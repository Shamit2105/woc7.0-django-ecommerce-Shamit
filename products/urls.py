from django.urls import path
from .views import (ItemCreateView,
                    ItemListView,ItemDetailView,SearchResultsListView,ReviewView)

urlpatterns = [
    path('', ItemListView.as_view(), name='home'),
    path('product/<int:pk>/', ItemDetailView.as_view(), name='product_detail'),
    path('review/<int:item_id>/', ReviewView.as_view(), name='review_form'),
    #path('create_category/<int:user_id>/',CategoryCreateView.as_view(),name='create_category'),
    #path('create_subcategory/<int:user_id>/',SubcategoryCreateView.as_view(),name='create_subcategory'),
    path('create_item/<int:user_id>/',ItemCreateView.as_view(),name='create_item'),
    path('searchresults/',SearchResultsListView.as_view(),name='search_results')
]
