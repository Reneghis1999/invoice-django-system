from django.shortcuts import render
from django.views import View
from fact_app.models import Invoice


class HomeView(View):
    """Main View"""

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.select_related('customer', 'created_by').all()

        context = {
            'invoices': invoices
        }

        return render(request, self.template_name, context)