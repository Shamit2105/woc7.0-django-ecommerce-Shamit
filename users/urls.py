from django.urls import path
from .views import SignUpView,PasswordResetFormView,PasswordResetRequestView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/<int:user_id>/', PasswordResetFormView.as_view(), name='password_reset_form'),
]
