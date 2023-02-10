from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favorite
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer, FavoriteSerializer



class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_superuser:
                return [IsAdminUser()]
            else:
                return [IsAuthenticated(), IsOwner()]
        else:
            return [IsAuthenticatedOrReadOnly()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(status="OPEN", draft=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def favorite_list(self, request):
            queryset = Favorite.objects.filter(user=request.auth.user)
            serializer = FavoriteSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def favorite_delete(self, request, pk=None):
        favorite = Favorite.objects.filter(user=self.request.user, advertisement=pk).first()
        if favorite is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite_add(self, request, pk=None):
        adv = self.get_object()
        user = self.request.user
        if adv.creator != user:
            favorite = Favorite.objects.filter(user=user, advertisement=adv).first()
            if favorite is None:
                Favorite.objects.create(user=user, advertisement=adv)
                return Response({'message': 'Запись добавлена в избранное!'})
            else:
                return Response({'ErrorMessage': 'Запись уже в избранном!'})
        else:
            return Response({'ErrorMessage': 'Вы не можете добавить свое объявление в избранное!'})