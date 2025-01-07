from django.urls import path
from .views import UserOrderCreateView,UserOrderBillView,UserOrderListView,AddToCartView,CartListView,CartDeleteView,CartOrderView

urlpatterns = [
    path('order/<int:item_id>/', UserOrderCreateView.as_view(), name='order'),
    path('bill/<int:pk>/', UserOrderBillView.as_view(), name='order_bill'),
    path('my-orders/', UserOrderListView.as_view(), name='my_orders'),
    path('add-to-cart/<int:item_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('cart/delete/<int:pk>/', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/order-all/', CartOrderView.as_view(), name='order_all_cart_items'),
]#je specific item ne add karvanu hoy tyare item_id, 

#delete cart ma cart ma item avi gai hati, etle pachi eni primary key(pk) e cart item 
#tarike ni ganaay