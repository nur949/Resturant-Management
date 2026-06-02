from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Order, Expense, MenuItem
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

import csv
from django.http import HttpResponse

def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Invoice', 'Date', 'Table', 'Staff', 'Status', 'Subtotal', 'Tax', 'Total'])
    
    last_30_days = timezone.now().date() - timedelta(days=30)
    orders = Order.objects.filter(created_at__date__gte=last_30_days).order_by('-created_at')
    
    for order in orders:
        writer.writerow([
            order.invoice_number,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            f"Table {order.table.number}",
            order.staff.username if order.staff else 'System',
            order.get_status_display(),
            order.subtotal,
            order.tax_amount,
            order.total_price
        ])
    
    return response

class ReportsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        
        # Sales Summary
        orders = Order.objects.filter(status='paid', created_at__date__gte=last_30_days)
        total_sales = sum(o.total_price for o in orders)
        context['total_sales'] = total_sales
        
        # Expense Summary
        expenses = Expense.objects.filter(date__gte=last_30_days)
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_expenses'] = total_expenses
        
        context['net_profit'] = total_sales - total_expenses
        
        # Popular Items
        context['popular_items'] = MenuItem.objects.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:5]
        
        # Daily Sales for last 7 days
        daily_sales = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            day_orders = Order.objects.filter(status='paid', created_at__date=date)
            amount = sum(o.total_price for o in day_orders)
            daily_sales.append({'date': date.strftime('%a'), 'amount': float(amount)})
        context['daily_sales_json'] = daily_sales
        
        return context
