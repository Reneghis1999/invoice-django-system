from django.db import models
from fact_app.models.base_model import BaseModel
from fact_app.models.invoice import Invoice

class Article(BaseModel):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        return self.quantity * self.unit_price