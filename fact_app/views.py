from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from fact_app.models import Invoice, Customer, Article


# ---------------------------
# HOME VIEW -> LISTVIEW
# ---------------------------
class HomeView(LoginRequiredMixin, ListView):
    """Afficher les factures avec pagination pour l'utilisateur connecté"""
    
    model = Invoice
    template_name = 'index.html'
    context_object_name = 'invoices'
    paginate_by = 5

    def get_queryset(self):
        """Filtrer les factures pour que l'utilisateur ne voie que les siennes"""
        return Invoice.objects.select_related('customer', 'created_by') \
                              .filter(created_by=self.request.user) \
                              .order_by('-created_at')


# ---------------------------
# CUSTOMER
# ---------------------------
class AddCustomerView(LoginRequiredMixin, View):
    """Ajouter un client"""

    template_name = "add_customer.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "address": request.POST.get("address"),
            "sex": request.POST.get("sex"),
            "age": request.POST.get("age"),
            "city": request.POST.get("city"),
            "zip_code": request.POST.get("zip"),
            "created_by": request.user
        }

        try:
            Customer.objects.create(**data)
            messages.success(request, "Customer registered successfully")
        except Exception as e:
            messages.error(request, f"Error creating customer: {e}")

        return redirect("add-customer")


# ---------------------------
# INVOICE
# ---------------------------
class AddInvoiceView(LoginRequiredMixin, View):
    """Créer une facture avec ses articles"""

    template_name = "add_invoice.html"

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.filter(created_by=request.user)
        return render(request, self.template_name, {"customers": customers})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customers = Customer.objects.filter(created_by=request.user)

        try:
            customer_id = request.POST.get("customer")
            invoice_type = request.POST.get("invoice_type")
            comment = request.POST.get("comment")

            articles = request.POST.getlist("article")
            qties = request.POST.getlist("qty")
            units = request.POST.getlist("unit")

            invoice = Invoice.objects.create(
                customer_id=customer_id,
                created_by=request.user,
                invoice_type=invoice_type,
                comments=comment,
                paid=False
            )

            items = [
                Article(
                    invoice=invoice,
                    name=name,
                    quantity=int(qties[idx]),
                    unit_price=float(units[idx])
                )
                for idx, name in enumerate(articles)
            ]

            Article.objects.bulk_create(items)

            messages.success(request, "Invoice created successfully")

        except Exception as e:
            messages.error(request, f"Error creating invoice: {e}")

        return render(request, self.template_name, {"customers": customers})


class UpdateInvoiceView(LoginRequiredMixin, View):
    """Modifier le statut paid"""

    def post(self, request, id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=id)

        if invoice.created_by != request.user:
            messages.error(request, "Unauthorized action")
            return redirect("home")

        try:
            invoice.paid = request.POST.get("paid") == "true"
            invoice.save()
            messages.success(request, "Invoice updated successfully")
        except Exception as e:
            messages.error(request, f"Error updating invoice: {e}")

        return redirect("home")


class DeleteInvoiceView(LoginRequiredMixin, View):
    """Supprimer une facture"""

    def post(self, request, id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=id)

        if invoice.created_by != request.user:
            messages.error(request, "Unauthorized action")
            return redirect("home")

        try:
            invoice.delete()
            messages.success(request, "Invoice deleted successfully")
        except Exception as e:
            messages.error(request, f"Error deleting invoice: {e}")

        return redirect("home")


class InvoiceVisualizationView(LoginRequiredMixin, View):
    """Visualiser une facture avec ses articles"""

    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(Invoice, pk=pk)

        # Vérifier que l'utilisateur est propriétaire de la facture
        if obj.created_by != request.user:
            messages.error(request, "Unauthorized action")
            return redirect("home")

        articles = obj.article_set.all()

        context = {
            'obj': obj,
            'articles': articles
        }

        return render(request, self.template_name, context)