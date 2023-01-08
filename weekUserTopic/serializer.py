from rest_framework import serializers

from weekUserTopic.models import WeekUserTopic


class WeekUserTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeekUserTopic
        fields = ['topic', 'phone', 'weeks']
