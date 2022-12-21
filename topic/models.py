from django.db import models
from category.models import Category
class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
