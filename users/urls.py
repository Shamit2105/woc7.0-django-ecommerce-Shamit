from django.urls import path
from .views import SignUpView,PasswordResetFormView,PasswordResetRequestView, PasswordChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password_change/<int:user_id>/', PasswordChangeView.as_view(), name='password_change'),
    path('password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset/<int:user_id>/', PasswordResetFormView.as_view(), name='password_reset_form'),

]
