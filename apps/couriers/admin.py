from django.contrib import admin
from .models import CourierProfile


@admin.register(CourierProfile)
class CourierProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car_type', 'is_working', 'preview_license', 'preview_selfie')
    list_filter = ('car_type', 'is_working')
    search_fields = ('user__full_name', 'user__phone', 'user__iin')

    def preview_license(self, obj):
        if obj.license_photo:
            return f"<img src='{obj.license_photo.url}' width='60' height='40' />"
        return "-"
    preview_license.allow_tags = True
    preview_license.short_description = 'Права'

    def preview_selfie(self, obj):
        if obj.selfie_photo:
            return f"<img src='{obj.selfie_photo.url}' width='60' height='60' />"
        return "-"
    preview_selfie.allow_tags = True
    preview_selfie.short_description = 'Селфи'
