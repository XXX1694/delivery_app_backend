from django.db import models
from apps.users.models import User


class CourierProfile(models.Model):
    """
    Профиль курьера. Один-к-одному связан с пользователем (User) с ролью 'courier'.
    Содержит специфичную информацию, которую не нужно хранить у всех пользователей.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='courier_profile',
        help_text="Связь с объектом User (роль должна быть 'courier')"
    )
    car_type = models.CharField(
        max_length=20,
        choices=[
            ('car', 'Легковой автомобиль'),
            ('truck', 'Грузовик'),
        ],
        help_text="Тип транспортного средства"
    )
    license_photo = models.ImageField(
        upload_to='couriers/licenses/',
        help_text="Фото водительского удостоверения"
    )
    selfie_photo = models.ImageField(
        upload_to='couriers/selfies/',
        help_text="Селфи курьера (для верификации)"
    )
    is_working = models.BooleanField(
        default=False,
        help_text="Курьер сейчас работает или нет"
    )

    def __str__(self):
        return f"Курьер: {self.user.full_name} | {'ВЫШЕЛ' if self.is_working else 'НЕ НА РАБОТЕ'}"
