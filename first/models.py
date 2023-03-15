import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Way(models.Model):
    """
    Основная модель для хранения путей

    :param user: Создатель маршрута
    :param arr: Список павильонов, через которые проходит маршрут
    :param distance: Длина маршрута
    :param time: Время на прохождение маршрута*
    :param created_at: Дата создания маршрута
    *\*Время пребывания в павильонах не учитывается.*
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    arr = models.TextField(default='')
    distance = models.TextField(default='')
    time = models.TextField(default='')
    created_at = models.DateField(default=datetime.datetime.now())