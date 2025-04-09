from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Swagger / Redoc
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Delivery App API",
        default_version='v1',
        description="Документация для API межгородской доставки",
        contact=openapi.Contact(email="support@delivery.kz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API приложения
    path('api/users/', include('apps.users.urls')),
    path('api/couriers/', include('apps.couriers.urls')),
    path('api/orders/', include('apps.orders.urls')),

    # Документация Swagger / Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Подключение media-файлов (фото курьеров, вложения)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)