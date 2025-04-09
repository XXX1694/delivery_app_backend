from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import random


class UserManager(BaseUserManager):
    def create_user(self, phone, full_name, iin, city, date_of_birth, role='client'):
        if not phone:
            raise ValueError("Телефон обязателен")
        user = self.model(
            phone=phone,
            full_name=full_name,
            iin=iin,
            city=city,
            date_of_birth=date_of_birth,
            role=role
        )
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, iin, city, date_of_birth, password=None):
        user = self.create_user(phone, full_name, iin, city, date_of_birth, role='manager')
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('courier', 'Курьер'),
        ('manager', 'Менеджер'),
    )

    phone = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)
    iin = models.CharField(max_length=12, unique=True)
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    # OTP
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['full_name', 'iin', 'city', 'date_of_birth']

    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_created = timezone.now()
        self.save()
        return self.otp_code

    def verify_otp(self, code):
        if not self.otp_code or self.otp_code != code:
            return False
        # Можно добавить проверку по времени
        return True
