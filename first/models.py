import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Pavilion(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.TextField()


class Way(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.datetime.now())