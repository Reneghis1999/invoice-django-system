from django.db import models
from django.contrib.auth.models import User
from fact_app.models.base_model import BaseModel
from fact_app.models.customer import Customer
from fact_app.enums.invoice_type import InvoiceType

class Invoice(BaseModel):

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)  # Le client de la facture
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)     # L'utilisateur qui a créé la facture
    paid = models.BooleanField(default=False)
    invoice_type = models.CharField(max_length=1, choices=InvoiceType.choices)
    comments = models.TextField(null=True, max_length=1000, blank=True)

    def __str__(self):
        return f"{self.customer.name} {self.created_at}"

    @property
    def get_total(self):
        articles = self.article_set.all()
        return sum(article.get_total for article in articles)