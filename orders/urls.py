from django.urls import path
from .views import UserOrderCreateView

urlpatterns = [
    path('order_create/', UserOrderCreateView.as_view(), name='order'),
]