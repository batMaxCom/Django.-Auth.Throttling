from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwner

from advertisements.serializers import AdvertisementSerializer
from advertisements.throttling import CustomAnonRateThrottle, CustomUserRateThrottle


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    # filter_backends = [OrderingFilter]
    # ordering_fields = ['created_at', 'status']
    throttle_classes = [AnonRateThrottle]
    # throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwner()]
        return []

