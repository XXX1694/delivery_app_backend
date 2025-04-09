from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    UserSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    Регистрирует нового пользователя или обновляет существующего,
    генерирует и отправляет OTP.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # вместо отправки SMS просто вернем код (для отладки)
        return Response({
            "message": "OTP-код отправлен",
            "otp": user.otp_code  # УДАЛИТЬ в продакшене!
        })


class VerifyOtpView(APIView):
    """
    Подтверждает OTP, возвращает токен.
    """
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })


class MeView(APIView):
    """
    Возвращает информацию о текущем пользователе.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
