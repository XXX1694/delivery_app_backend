from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CourierProfile
from .serializers import CourierProfileSerializer
from apps.users.models import User


class CourierProfileMeView(generics.RetrieveUpdateAPIView):
    """
    Получить или обновить СВОЙ профиль курьера.
    """
    serializer_class = CourierProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CourierProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()


class CourierWorkToggleView(APIView):
    """
    Курьер вручную меняет статус 'работает / не работает'.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            profile = request.user.courier_profile
        except CourierProfile.DoesNotExist:
            return Response({"error": "Профиль курьера не найден."}, status=404)

        profile.is_working = not profile.is_working
        profile.save()

        return Response({
            "message": "Статус обновлён",
            "is_working": profile.is_working
        })


class ActiveCouriersListView(generics.ListAPIView):
    """
    Менеджер или админ получает список всех активных курьеров.
    """
    serializer_class = CourierProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return CourierProfile.objects.filter(is_working=True)
