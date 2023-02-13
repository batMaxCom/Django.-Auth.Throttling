from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        req = self.context
        user = req['request'].user
        request = req['view'].action
        if request == 'create' or data.get('status') == 'OPEN':
            if Advertisement.objects.filter(creator=user, status='OPEN').count() > 9:
                raise serializers.ValidationError('У пользователя не может быть больше 10 активных объявлений!')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer()

    class Meta:
        model = Favorite
        fields = ['advertisement']