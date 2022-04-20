from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Advertisement.objects.filter(creator=user, status='OPEN').count() < 10:
                return data
            else:
                raise serializers.ValidationError('The maximum number of open ads is 10')
        if self.context['request'].method == 'PATCH' and Advertisement.objects.filter(status='OPEN').count() >= 1:
            status = Advertisement.objects.get(id=self.context['request'].parser_context['kwargs']['pk']).status
            ads_count = Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN').count()
            if status != data['status'] and ads_count < 10:
                return data
            elif status != data['status'] and ads_count == 10 and status == 'OPEN':
                return data
            elif status != data['status'] and ads_count == 10 and status == 'CLOSED':
                raise serializers.ValidationError('The maximum number of open ads is 10')
            else:
                raise serializers.ValidationError('Change Error')
