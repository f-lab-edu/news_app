from rest_framework import viewsets
from rest_framework.response import Response

from django.db.models import Count, Q

from user.models import User
from user.serializers import UserSerializer

from topic.models import Topic

from weekUserTopic.serializer import WeekUserTopicSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
