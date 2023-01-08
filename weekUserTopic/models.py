from django.db import models
from topic.models import Topic
from user.models import User
import datetime

class WeekUserTopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weeks = models.IntegerField(null=True)