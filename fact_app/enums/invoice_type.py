from django.db import models

class InvoiceType(models.TextChoices):
    RECEIPT = "R", "RECU"
    PROFORMA = "P", "PROFORMA FACTURE"
    FACTURE = "F", "FACTURE"