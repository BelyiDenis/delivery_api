"""
Декораторы для автоматического логирования действий пользователей
"""

from functools import wraps
from .models import Log


def get_client_ip(request):
    """Получение IP адреса клиента из запроса"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_action(action):
    """
    Декоратор для логирования действий в ViewSet.
    Использование: @log_action('CREATE')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Выполняем исходный метод
            response = func(self, request, *args, **kwargs)

            # Логируем только успешные действия (статус 2xx)
            if request.user and request.user.is_authenticated and 200 <= response.status_code < 300:
                # Определяем название модели
                if hasattr(self, 'get_queryset') and hasattr(self.get_queryset(), 'model'):
                    model_name = self.get_queryset().model.__name__
                else:
                    model_name = 'Unknown'

                # Определяем ID объекта
                object_id = ''
                if 'pk' in kwargs:
                    object_id = str(kwargs['pk'])
                elif hasattr(response, 'data') and isinstance(response.data, dict):
                    if 'id' in response.data:
                        object_id = str(response.data['id'])
                    elif 'id_delivery_request' in response.data:
                        object_id = str(response.data['id_delivery_request'])
                    elif 'id_upd' in response.data:
                        object_id = str(response.data['id_upd'])

                # Создаём запись в логе
                Log.objects.create(
                    user=request.user,
                    action=action,
                    model_name=model_name,
                    object_id=object_id,
                    ip_address=get_client_ip(request)
                )

            return response
        return wrapper
    return decorator
