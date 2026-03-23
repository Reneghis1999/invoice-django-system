from django.db import models
from django.contrib.auth.models import User
from fact_app.models.base_model import BaseModel 


class Customer(BaseModel):

    SEX_TYPES = (
        ('M', 'Masculin'),
        ('F', 'Feminin'),
    )

    AGE_CHOICES = (
        ('0-15', '0-15'),
        ('15-25', '15-25'),
        ('25-40', '25-40'),
        ('40+', '40+'),
    )

    name = models.CharField(max_length=132)
    email = models.EmailField()
    phone = models.CharField(max_length=132)
    address = models.CharField(max_length=64)
    sex = models.CharField(max_length=1, choices=SEX_TYPES)
    age = models.CharField(max_length=10, choices=AGE_CHOICES)  # corrigé
    city = models.CharField(max_length=32)
    zip_code = models.CharField(max_length=16)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name