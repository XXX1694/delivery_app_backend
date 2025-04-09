from rest_framework import serializers
from .models import User
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'iin', 'city', 'date_of_birth', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'iin', 'city', 'date_of_birth']

    def create(self, validated_data):
        phone = validated_data['phone']
        # если пользователь уже есть — генерируем новый OTP
        user, created = User.objects.get_or_create(phone=phone, defaults=validated_data)
        if not created:
            # обновим данные, если пользователь уже существует
            for key, value in validated_data.items():
                setattr(user, key, value)
            user.save()
        user.generate_otp()
        return user


class VerifyOtpSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone = data['phone']
        otp = data['otp_code']
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not user.verify_otp(otp):
            raise serializers.ValidationError("Неверный или просроченный OTP")

        data['user'] = user
        return data
