from django.db import models
from userNews.models import UserNews


class ReadingTime(models.Model):
    user_news = models.ForeignKey(UserNews, on_delete=models.CASCADE)
    reading_time = models.IntegerField(max_length=200)

