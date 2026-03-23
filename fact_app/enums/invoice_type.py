from django.db import models

class InvoiceType(models.TextChoices):
    RECEIPT = "R", "RECIEPT"
    PROFORMA = "P", "PROFORMA INVOICE"
    FACTURE = "I", "INVOICE"