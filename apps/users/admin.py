from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'phone', 'full_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('phone', 'full_name', 'iin')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('phone', 'full_name', 'iin', 'city', 'date_of_birth', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('OTP', {'fields': ('otp_code', 'otp_created')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'iin', 'city', 'date_of_birth', 'role', 'password1', 'password2')}
         ),
    )
    readonly_fields = ('otp_code', 'otp_created')
