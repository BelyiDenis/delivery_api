"""
Главный файл маршрутизации URL
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger документация API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),

    # Сиквенс №20: Токен (получение) - POST /api/v1/auth/token/
    # Сиквенс №21: Токен (обновление) - POST /api/v1/auth/token/refresh/
    path('api/v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),

    # API приложений
    path('api/v1/', include('upd.urls')),
    path('api/v1/', include('delivery_requests.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('vehicles.urls')),
    path('api/v1/', include('routes.urls')),
    path('api/v1/', include('waybills.urls')),
    path('api/v1/', include('photos.urls')),
    path('api/v1/', include('signatures.urls')),
    path('api/v1/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
