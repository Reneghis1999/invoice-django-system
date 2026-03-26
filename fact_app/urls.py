from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('add-customer/', views.AddCustomerView.as_view(), name='add-customer'),

    path('add-invoice/', views.AddInvoiceView.as_view(), name='add-invoice'),

    path('invoice/update/<uuid:id>/', views.UpdateInvoiceView.as_view(), name='update-invoice'),

    path('invoice/delete/<uuid:id>/', views.DeleteInvoiceView.as_view(), name='delete-invoice'),
    
    path('view-invoice/<uuid:pk>/', views.InvoiceVisualizationView.as_view(), name='view-invoice'),
]