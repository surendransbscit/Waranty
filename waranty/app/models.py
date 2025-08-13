from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='customuser_permissions', 
        blank=True
    )


class details(models.Model):
    serial_number = models.CharField(max_length=50, unique=True)
    invoice = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    chno = models.CharField(max_length=100, null=True)
    motor = models.CharField(max_length=100, null=True)
    controller = models.CharField(max_length=100, null=True)
    charge = models.CharField(max_length=50 , null=True)
    battery_no = models.CharField(max_length=100 , null=True)
    customer_name = models.CharField(max_length=100)
    address = models.TextField( null=True)
    phone_number = models.BigIntegerField()
    purchase_date = models.DateField()
    type = models.CharField(max_length=50, null=True,default=None)
    remark = models.TextField(blank=True, null=True,default=None)
    email = models.CharField(max_length=50,null=True ,default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} - {self.customer_name}"

    class Meta:
        db_table = 'customer_details'