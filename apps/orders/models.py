from django.db import models
from apps.users.models import User


class Order(models.Model):
    """
    Заказ на доставку. Создаётся клиентом, выполняется курьером.
    Хранит все ключевые данные маршрута и груза.
    """
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        limit_choices_to={'role': 'client'},
        help_text="Пользователь, оформивший заказ (только клиенты)"
    )
    courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_orders',
        limit_choices_to={'role': 'courier'},
        help_text="Назначенный курьер (назначается позже менеджером)"
    )

    pickup_address = models.TextField(help_text="Адрес отправления")
    pickup_lat = models.FloatField(help_text="Широта точки отправления")
    pickup_lng = models.FloatField(help_text="Долгота точки отправления")

    delivery_address = models.TextField(help_text="Адрес доставки")
    delivery_lat = models.FloatField(help_text="Широта точки доставки")
    delivery_lng = models.FloatField(help_text="Долгота точки доставки")

    dimensions = models.CharField(max_length=255, help_text="Габариты или описание груза")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Стоимость доставки")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания заказа")
    updated_at = models.DateTimeField(auto_now=True, help_text="Время последнего обновления")

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('assigned', 'Назначен курьер'),
        ('in_progress', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        help_text="Текущий статус заказа"
    )

    def __str__(self):
        return f"{self.id} | {self.client.full_name} → {self.delivery_address} | {self.status}"


class OrderStatusHistory(models.Model):
    """
    История изменения статусов заказа. Хранит каждый шаг.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Заказ {self.order.id} → {self.status} в {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class OrderAttachment(models.Model):
    """
    Фотографии и вложения к заказу (например, фото груза).
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='attachments')
    image = models.ImageField(upload_to='orders/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Аттач к заказу #{self.order.id}"
