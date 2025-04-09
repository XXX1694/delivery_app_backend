from rest_framework import serializers
from .models import CourierProfile
from apps.users.serializers import UserSerializer


class CourierProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор профиля курьера. Включает вложенные данные пользователя (read-only).
    Поддерживает загрузку фото и обновление статуса.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = CourierProfile
        fields = [
            'id',
            'user',
            'car_type',
            'license_photo',
            'selfie_photo',
            'is_working',
        ]
        read_only_fields = ['user']
