from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Expense(models.Model):
    amount = models.FloatField(verbose_name='Сумма')
    date = models.DateField(default=now, verbose_name='Дата')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    
    class Meta:
        ordering: ['date']


class Income(models.Model):
    amount = models.FloatField(verbose_name='Сумма')  # DECIMAL
    date = models.DateField(default=now, verbose_name='Дата')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey('Source', on_delete=models.CASCADE, verbose_name='Источник')

    class Meta:
        ordering: ['date']


class Source(models.Model):
    name = models.CharField(max_length=255, verbose_name='Источник')

    def __str__(self):
        return self.name

class WishesList(models.Model):
    amount = models.FloatField(verbose_name='Стоимость')  # DECIMAL
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)