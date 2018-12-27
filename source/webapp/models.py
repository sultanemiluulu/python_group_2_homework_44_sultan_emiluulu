from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee', verbose_name='User')
    phone = models.CharField(max_length=50, verbose_name='Phone')

    def __str__(self):
        return self.user.get_full_name()


class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Description')
    photo = models.ImageField(verbose_name='Image')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.name
