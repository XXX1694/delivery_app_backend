from django.urls import path
from .views import RegisterView, VerifyOtpView, MeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('me/', MeView.as_view(), name='me'),
]
