from django.db import models
from topic.models import Topic
from user.models import User

class WeekUserTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.CharField(max_length=10)
