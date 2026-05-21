from rest_framework import viewsets, permissions
from .models import Route
from .serializers import RouteSerializer


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]
