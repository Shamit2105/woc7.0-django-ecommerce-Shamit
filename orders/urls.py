from django.urls import path
from .views import UserOrderCreateView,UserOrderBillView,UserOrderListView,AddToCartView,CartListView

urlpatterns = [
    path('order/<int:item_id>/', UserOrderCreateView.as_view(), name='order'),
    path('bill/<int:pk>/', UserOrderBillView.as_view(), name='order_bill'),
    path('my-orders/', UserOrderListView.as_view(), name='my_orders'),
    path('add-to-cart/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartListView.as_view(), name='cart'),
]