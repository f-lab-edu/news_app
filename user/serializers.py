from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    # def validate(self, valid_data):
    #     pass
    CATEGORY = (
        ('Society', '사회'),
        ('IT', 'IT'),
        ('Politics', '정치'),
        ('Economy', '경제')
    )

    category1 = serializers.ChoiceField(choices=CATEGORY)
    category2 = serializers.ChoiceField(choices=CATEGORY)
    category3 = serializers.ChoiceField(choices=CATEGORY)

    class Meta:
        model = User
        fields = ['phone', 'name', 'password', 'category1', 'category2', 'category3']
