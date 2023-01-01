from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_date):
        user = User.objects.create_user(
            phone=validated_date['phone'],
            name=validated_date['name'],
            password=validated_date['password']
        )
        return user

    class Meta:
        model = User
        fields = ['phone', 'name', 'is_active', 'is_superuser']