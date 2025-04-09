from rest_framework import serializers
from .models import Order, OrderStatusHistory, OrderAttachment
from apps.users.serializers import UserSerializer


class OrderAttachmentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для фотографий и файлов, прикреплённых к заказу.
    Используется для отображения вложений в заказе.
    """
    class Meta:
        model = OrderAttachment
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для истории изменений статуса заказа.
    Выводится как вложенный объект в заказ.
    """
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'timestamp', 'comment']
        read_only_fields = ['id', 'timestamp']


class OrderSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор заказа.
    Включает вложенные данные клиента, курьера, вложения и историю.
    """
    client = UserSerializer(read_only=True)
    courier = UserSerializer(read_only=True)

    # вложенные связи — только на чтение
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    attachments = OrderAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'client',
            'courier',
            'pickup_address',
            'pickup_lat',
            'pickup_lng',
            'delivery_address',
            'delivery_lat',
            'delivery_lng',
            'dimensions',
            'price',
            'status',
            'created_at',
            'updated_at',
            'status_history',
            'attachments'
        ]
        read_only_fields = ['id', 'client', 'courier', 'created_at', 'updated_at', 'status_history', 'attachments']

    def create(self, validated_data):
        """
        При создании заказа автоматически привязываем клиента из request.user.
        """
        user = self.context['request'].user
        validated_data['client'] = user
        return super().create(validated_data)
