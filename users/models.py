"""
Модели приложения users.
Соответствует инфологической модели: таблицы Пользователь, Водитель, Менеджер, Диспетчер
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя"""

    def create_user(self, phone, password=None, **extra_fields):
        """Создание обычного пользователя"""
        if not phone:
            raise ValueError('Телефон обязателен')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """Создание суперпользователя (администратора)"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', 1)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    Аутентификация по телефону вместо email/username.
    """

    ROLE_CHOICES = [
        ('driver', 'Водитель'),
        ('manager', 'Менеджер'),
        ('dispatcher', 'Диспетчер'),
        ('admin', 'Администратор'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='ID пользователя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    middle_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Отчество')
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, default='driver', verbose_name='Роль')
    phone = models.CharField(
        max_length=20, unique=True, verbose_name='Телефон')
    email = models.CharField(max_length=100, unique=True,
                             blank=True, null=True, verbose_name='Email')
    is_active = models.IntegerField(default=1, verbose_name='Активен')
    is_staff = models.BooleanField(
        default=False, verbose_name='Доступ в админку')
    is_superuser = models.BooleanField(
        default=False, verbose_name='Суперпользователь')
    last_login_date = models.DateTimeField(
        auto_now=True, verbose_name='Последний вход')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.phone})'


class Driver(models.Model):
    """
    Модель водителя (расширение пользователя с ролью driver).
    Связь 1:1 с User.
    """
    id_driver = models.AutoField(primary_key=True)
    id_user = models.OneToOneField(
        User, on_delete=models.CASCADE, db_column='id_user')
    driver_license_number = models.CharField(
        max_length=10, verbose_name='Номер ВУ')

    class Meta:
        db_table = 'driver'

    def __str__(self):
        return f'{self.id_user.last_name} {self.id_user.first_name}'


class Manager(models.Model):
    """
    Модель менеджера (расширение пользователя с ролью manager).
    Связь 1:1 с User.
    """
    id_manager = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column='id_manager')
    department_name = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Отдел')

    class Meta:
        db_table = 'manager'


class Dispatcher(models.Model):
    """
    Модель диспетчера (расширение пользователя с ролью dispatcher).
    Связь 1:1 с User.
    """
    SHIFT_CHOICES = [
        ('morning', 'Утро'),
        ('evening', 'Вечер'),
        ('night', 'Ночь'),
    ]
    id_dispatcher = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, db_column='id_dispatcher')
    shift_name = models.CharField(
        max_length=20, choices=SHIFT_CHOICES, blank=True, null=True, verbose_name='Смена')

    class Meta:
        db_table = 'dispatcher'
