from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='employee', verbose_name='User')
    phone = models.CharField(max_length=50, verbose_name='Phone')

    def __str__(self):
        return self.user.get_full_name()
