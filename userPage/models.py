from django.db import models
from userNews.models import UserNews

class UserPage(models.Model):
    user_news1 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news1')
    user_news2 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news2')
    user_news3 = models.ForeignKey(UserNews, on_delete=models.CASCADE, related_name='user_news3')
