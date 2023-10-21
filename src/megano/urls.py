from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Items API",
      default_version='v1',
      description="Описание проекта",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@company.local"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("frontend.urls")),
    path("api/", include("src.api_shop.urls")),
    path("api/sign-", include("src.api_user.urls")),
    # Документация Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # path('', include(router.urls)),
]

if settings.DEBUG:
    # Обслуживание медиа-файлов
    urlpatterns.extend(
        static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        ),
    )

    # Вывод статических файлов
    urlpatterns.extend(
        static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT
        )
    )

# Переопределяем шапку в админке
admin.site.site_header = "Админка Megano"
