from django.urls import path
from .views import CourierProfileMeView, CourierWorkToggleView, ActiveCouriersListView

urlpatterns = [
    path('me/', CourierProfileMeView.as_view(), name='courier-me'),
    path('toggle-status/', CourierWorkToggleView.as_view(), name='courier-toggle-status'),
    path('active/', ActiveCouriersListView.as_view(), name='courier-active'),
]
