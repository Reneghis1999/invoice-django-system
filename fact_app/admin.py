from django.contrib import admin
from .models import *

class AdminCustomer(admin.ModelAdmin):
    list_display = ('name','email','phone','address','sex','age','city','zip_code')

class AdminInvoice(admin.ModelAdmin):
    list_display = (
        'customer', 
        'created_by',     # remplace save_by
        'created_at',     # remplace invoice_date_time
        'get_total',      # calcule le total via property
        'updated_at',     # remplace last_updated_date
        'paid',
        'invoice_type'
    )

class AdminArticle(admin.ModelAdmin):
    list_display = ('invoice','name','quantity','unit_price','get_total')  # property ok

admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article, AdminArticle)