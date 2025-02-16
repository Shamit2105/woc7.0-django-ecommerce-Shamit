from django.urls import path
from .views import (
    OrderView, UserOrderBillView, OrderConfirmView, PreviousOrderListView,OrderLView,
    AddToCartView, CartListView, CartDeleteView, CartOrderView,
    DecreaseQuantityView, IncreaseQuantityView, OrderIncreaseQuantityView,OrderDecreaseQuantityView
    ,CancelOrderView
)

urlpatterns = [
    path('order_summary/<int:item_id>', OrderConfirmView.as_view(), name='order_confirm'),
    path('order_s', OrderLView.as_view(), name='order'),
    path('order/', OrderView.as_view(), name='order_form'),
    path('order/increase/<int:pk>/', OrderIncreaseQuantityView.as_view(), name='order_increase'),
    path('order/decrease/<int:pk>/', OrderDecreaseQuantityView.as_view(), name='order_decrease'),
    path('bill/<int:pk>/', UserOrderBillView.as_view(), name='order_bill'),
    path('my-orders/', PreviousOrderListView.as_view(), name='my_orders'),
    path('add-to-cart/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/order-all/', CartOrderView.as_view(), name='order_all_cart_items'),
    path('cart/increase/<int:pk>/', IncreaseQuantityView.as_view(), name='cart_increase'),
    path('cart/decrease/<int:pk>/', DecreaseQuantityView.as_view(), name='cart_decrease'),  
    path('cancel_order/<int:order_id>/', CancelOrderView.as_view(), name='cancel_order'),
]