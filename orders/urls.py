from django.urls import path
from .views import UserOrderCreateView

urlpatterns = [
    path('order/<int:item_id>/', UserOrderCreateView.as_view(), name='order'),
]