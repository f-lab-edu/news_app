from django.db import models
from news.models import News
from weekUserTopic.models import WeekUserTopic

class UserNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    week_user_topic = models.ForeignKey(WeekUserTopic, on_delete=models.CASCADE)

