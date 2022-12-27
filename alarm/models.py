from django.db import models
from userPage.models import UserPage


class Alarm(models.Model):
    user_page = models.ForeignKey(UserPage, on_delete=models.CASCADE)
    send_date = models.DateTimeField()

