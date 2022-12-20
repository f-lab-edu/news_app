from django.db import models
from topic.models import Topic

class News(models.Model):
    topic1 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic1')
    topic2 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic2')
    topic3 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topic3')
    link = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
