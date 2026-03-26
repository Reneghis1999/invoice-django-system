from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from fact_app.models import Invoice, Customer, Article
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator


class HomeView(View):
    """Afficher les factures avec pagination"""

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        invoices_list = Invoice.objects.select_related(
            "customer", "created_by"
        ).filter(
            created_by=request.user
        ).order_by("-created_at")

        paginator = Paginator(invoices_list, 5)
        page = request.GET.get("page")

        invoices = paginator.get_page(page)

        context = {
            "invoices": invoices
        }

        return render(request, self.template_name, context)


class AddCustomerView(View):
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


class AddInvoiceView(View):
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


class UpdateInvoiceView(View):
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


class DeleteInvoiceView(View):
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
    
class InvoiceVisualizationView(View):
    """ This view helps to visualize the invoices """

    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        obj = Invoice.objects.get(pk=pk)

        articles = obj.article_set.all()

        context = {
            'obj': obj,
            'articles' : articles
        }

        return render(request, self.template_name, context)
    
    

