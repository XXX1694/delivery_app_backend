from django.contrib import admin
from .models import Order, OrderStatusHistory, OrderAttachment


class OrderStatusInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('timestamp',)


class OrderAttachmentInline(admin.TabularInline):
    model = OrderAttachment
    extra = 0
    readonly_fields = ('preview_image', 'uploaded_at')

    def preview_image(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='80' />"
        return "-"
    preview_image.allow_tags = True
    preview_image.short_description = 'Изображение'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'courier', 'pickup_address_short', 'delivery_address_short', 'price', 'status')
    list_filter = ('status', 'courier__courier_profile__is_working')
    search_fields = ('pickup_address', 'delivery_address', 'client__full_name', 'courier__full_name')
    inlines = [OrderStatusInline, OrderAttachmentInline]

    def pickup_address_short(self, obj):
        return obj.pickup_address[:30] + '...'

    def delivery_address_short(self, obj):
        return obj.delivery_address[:30] + '...'

    pickup_address_short.short_description = 'Откуда'
    delivery_address_short.short_description = 'Куда'


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'timestamp', 'comment')
    list_filter = ('status', 'timestamp')
    search_fields = ('order__client__full_name', 'comment')


@admin.register(OrderAttachment)
class OrderAttachmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'uploaded_at', 'preview_image')

    def preview_image(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='80' />"
        return "-"
    preview_image.allow_tags = True
    preview_image.short_description = 'Файл'
