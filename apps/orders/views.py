from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, OrderStatusHistory
from .serializers import OrderSerializer
from apps.users.models import User


# ------------------ Permissions ------------------

class IsClient(permissions.BasePermission):
    """
    Разрешает доступ только клиентам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'


class IsCourier(permissions.BasePermission):
    """
    Разрешает доступ только курьерам.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'courier'


class IsManager(permissions.BasePermission):
    """
    Только для is_staff менеджеров.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


# ------------------ Вьюхи заказов ------------------

class ClientOrderListCreateView(generics.ListCreateAPIView):
    """
    Клиент может:
    - GET: Получить список своих заказов
    - POST: Создать новый заказ
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('-created_at')


class CourierOrderListView(generics.ListAPIView):
    """
    Курьер получает список только тех заказов, которые ему назначили.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsCourier]

    def get_queryset(self):
        return Order.objects.filter(courier=self.request.user).order_by('-created_at')


class AssignCourierView(APIView):
    """
    Менеджер вручную назначает курьера на заказ.
    """
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def post(self, request, order_id):
        courier_id = request.data.get('courier_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден"}, status=404)

        try:
            courier = User.objects.get(id=courier_id, role='courier')
        except User.DoesNotExist:
            return Response({"detail": "Курьер не найден"}, status=404)

        order.courier = courier
        order.status = 'assigned'
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status='assigned',
            comment=f"Курьер {courier.full_name} назначен менеджером"
        )

        return Response({"detail": f"Курьер {courier.full_name} назначен"}, status=200)


class UpdateOrderStatusView(APIView):
    """
    Курьер обновляет статус заказа (например, начал доставку или доставил).
    """
    permission_classes = [permissions.IsAuthenticated, IsCourier]

    def post(self, request, order_id):
        status_code = request.data.get("status")
        comment = request.data.get("comment", "")

        try:
            order = Order.objects.get(id=order_id, courier=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден или не принадлежит вам"}, status=404)

        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if status_code not in valid_statuses:
            return Response({"detail": "Недопустимый статус"}, status=400)

        order.status = status_code
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=status_code,
            comment=comment
        )

        return Response({"detail": "Статус обновлён", "status": status_code}, status=200)
