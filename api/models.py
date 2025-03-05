from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class ApiUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('provider', 'Поставщик'),
        ('consumer', 'Потребитель'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

class Warehouse(models.Model):
    name = models.CharField(max_length=128)

class Product(models.Model):
    name = models.CharField(max_length=128)
    warehouse = models.ForeignKey(Warehouse, related_name="products", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('supply', 'Поставка'),
        ('consume', 'Забор'),
    )
    product = models.ForeignKey(Product, related_name='transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(ApiUser, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.transaction_type == 'consume' and self.quantity > self.product.quantity:
            raise ValidationError("Недостаточно товара на складе")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.transaction_type == 'supply':
            self.product.quantity += self.quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)