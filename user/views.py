from rest_framework import viewsets
from rest_framework.response import Response

from django.db import DatabaseError, transaction

from user.models import User
from user.serializers import UserSerializer

from weekUserTopic.serializer import WeekUserTopicSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            phone = serializer.data.phone
            name = serializer.data.name
            password = serializer.data.password
            category1 = serializer.data.category1
            category2 = serializer.data.category2
            category3 = serializer.data.category3

            if self.queryset.filter(phone=phone).exists():
                return Response(data={'detail': 'This user already has a profile'}, status=400)

            if category1 == category2 or category2 == category3 or category1 == category3:
                return Response(data={'detail: 서로 다른 카테고리를 선택해주세요.'}, status=400)

            topic1, topic2, topic3 = User.objects.create(phone=phone, name=name, password=password, category1=category1,
                                                         category2=category2, category3=category3)

            try:
                with transaction.atomic():
                    week_user_topic_data = [
                        {'topic': topic1, 'user': phone, 'weeks': 0},
                        {'topic': topic2, 'user': phone, 'weeks': 0},
                        {'topic': topic3, 'user': phone, 'weeks': 0},
                    ]
                    week_user_topic_serializer = WeekUserTopicSerializer(data=week_user_topic_data, many=True)
                    if not week_user_topic_serializer.is_valid():
                        return Response({'detail': 'is not valid'}, 400)
                    week_user_topic_serializer.save()
            except DatabaseError:
                raise Exception('week_user_topic db error.')

            return Response(serializer.data, 200)
        else:
            return Response({'detail': 'is not valid'}, 400)
