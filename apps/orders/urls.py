from django.urls import path
from .views import (
    ClientOrderListCreateView,
    CourierOrderListView,
    AssignCourierView,
    UpdateOrderStatusView
)

urlpatterns = [
    # Клиент: создать заказ и получить список своих
    path('', ClientOrderListCreateView.as_view(), name='client-orders'),

    # Курьер: получить список назначенных заказов
    path('my/', CourierOrderListView.as_view(), name='courier-orders'),

    # Менеджер: назначить курьера на заказ
    path('<int:order_id>/assign/', AssignCourierView.as_view(), name='assign-courier'),

    # Курьер: обновить статус доставки
    path('<int:order_id>/update-status/', UpdateOrderStatusView.as_view(), name='update-status'),
]
