from django.db import models


class Route(models.Model):
    id_route = models.AutoField(primary_key=True)
    loading_address_warehouse = models.CharField(max_length=500)
    unloading_address_client = models.CharField(max_length=500)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2)
    planned_duration_minutes = models.IntegerField()

    class Meta:
        db_table = 'route'

    def __str__(self):
        return f'{self.loading_address_warehouse} -> {self.unloading_address_client}'
