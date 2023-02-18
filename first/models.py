import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Way(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    arr = models.TextField(default='')
    distance = models.TextField(default='')
    time = models.TextField(default='')
    created_at = models.DateField(default=datetime.datetime.now())