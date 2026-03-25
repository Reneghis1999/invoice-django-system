from django.shortcuts import render
from django.views import View
from fact_app.models import Invoice, Customer, Article
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class HomeView(View):
    """Main View: affiche toutes les factures avec pagination"""

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # Ici On ordonne les factures par date de création décroissante
        invoices_list = Invoice.objects.select_related('customer', 'created_by').order_by('-created_at')

        # Pagination : on a 5 factures par page
        paginator = Paginator(invoices_list, 5)
        page = request.GET.get('page')

        try:
            invoices = paginator.page(page)
        except PageNotAnInteger:
            invoices = paginator.page(1)
        except EmptyPage:
            invoices = paginator.page(paginator.num_pages)

        context = {
            'invoices': invoices
        }

        return render(request, self.template_name, context)


class AddCustomerView(View):
    """Ajouter un nouveau client"""

    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = {

            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'created_by': request.user
        }

        try:
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, "Customer registered successfully")
            else:
                messages.error(request, "Sorry, please try again. The sent data is corrupt")
        except Exception as e:
            messages.error(request, f"Sorry, an error occurred: {e}")

        return render(request, self.template_name)


class AddInvoiceView(View):
    """Ajouter une nouvelle facture avec ses articles"""

    template_name = 'add_invoice.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.filter(created_by=request.user)
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        customers = Customer.objects.filter(created_by=request.user)
        context = {
            'customers': customers
        }

        try:
            # Données de la facture
            customer_id = request.POST.get('customer')
            invoice_type = request.POST.get('invoice_type')
            comment = request.POST.get('comment')

            # Listes d'articles
            articles = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')

            # Créer la facture
            invoice = Invoice.objects.create(
                customer_id=customer_id,
                created_by=request.user,
                invoice_type=invoice_type,
                comments=comment,
                paid=False  # on a par défaut unpaid
            )

            # Créer tous les articles liés
            items = [
                Article(
                    invoice=invoice,
                    name=name,
                    quantity=int(qties[idx]),
                    unit_price=float(units[idx])
                ) for idx, name in enumerate(articles)
            ]

            Article.objects.bulk_create(items)
            messages.success(request, "Invoice and items saved successfully!")

        except Exception as e:
            messages.error(request, f"Sorry, an error occurred: {e}")

        return render(request, self.template_name, context)