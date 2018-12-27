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


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PREPARING = 'preparing'
    STATUS_ON_WAY = 'on_way'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_ON_WAY, 'On way'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELED, 'Canceled')
    )

    contact_phone = models.CharField(max_length=50, verbose_name='Contact Phone')
    contact_name = models.CharField(max_length=100, verbose_name='Contact Name')
    delivery_address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Delivery Address')
    status = models.CharField(max_length=20, default=STATUS_NEW, verbose_name='Status', choices=STATUS_CHOICES)
    operator = models.ForeignKey(User, null=True, blank=True, related_name='orders', verbose_name='Operator', on_delete=models.PROTECT)
    courier = models.ForeignKey(User, null=True, blank=True, related_name='delivered', verbose_name='Courier', on_delete=models.PROTECT)

    def __str__(self):
        return self.contact_phone

