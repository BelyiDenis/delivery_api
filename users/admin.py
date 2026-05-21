from django.contrib import admin
from .models import User, Driver, Manager, Dispatcher


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name',
                    'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('last_name', 'first_name', 'phone')


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('id_driver', 'id_user', 'driver_license_number')


admin.site.register(Manager)
admin.site.register(Dispatcher)
