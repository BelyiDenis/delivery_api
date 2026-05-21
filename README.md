cat > README.md << 'EOF'
# Delivery API

REST API для автоматизации обработки заявок на доставку пиломатериалов.

## Технологии

- Python 3.11
- Django 5.0.6
- Django REST Framework 3.15.1
- JWT аутентификация
- SQLite (прототип)

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <your-repo-url>
cd delivery_api

# Посмотреть логи всех контейнеров
docker-compose logs -f

# Посмотреть логи только Django
docker-compose logs -f django-api

# Перезапустить контейнеры
docker-compose restart

# Остановить все контейнеры
docker-compose down

# Запустить снова
docker-compose up -d

# Зайти внутрь Django контейнера
docker-compose exec django-api bash

# Выполнить команду в Django
docker-compose exec django-api python manage.py <command>