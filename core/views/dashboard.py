from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, F
from datetime import timedelta
from ..models import Order, Table, Expense, Ingredient, Reservation

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        # Basic Metrics
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status='pending').count()
        context['total_tables'] = Table.objects.count()
        context['available_tables'] = Table.objects.filter(status='available').count()
        context['occupied_tables'] = context['total_tables'] - context['available_tables']
        context['recent_orders'] = Order.objects.order_by('-created_at')[:5]
        
        # Financial Metrics (Today)
        today_paid_orders = Order.objects.filter(created_at__date=today, status='paid')
        context['today_sales'] = sum(order.total_price for order in today_paid_orders)
        context['today_expenses'] = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Financial Metrics (Month)
        month_paid_orders = Order.objects.filter(created_at__date__gte=start_of_month, status='paid')
        context['month_sales'] = sum(order.total_price for order in month_paid_orders)
        context['month_expenses'] = Expense.objects.filter(date__gte=start_of_month).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Operations & Inventory
        context['low_stock_count'] = Ingredient.objects.filter(current_stock__lte=F('low_stock_threshold')).count()
        context['today_reservations_count'] = Reservation.objects.filter(date=today).count()
        
        # Chart Data (Last 7 Days)
        days = []
        revenue_data = []
        expense_data = []
        
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            days.append(date.strftime('%a'))
            
            day_sales = sum(order.total_price for order in Order.objects.filter(created_at__date=date, status='paid'))
            day_expenses = Expense.objects.filter(date=date).aggregate(Sum('amount'))['amount__sum'] or 0
            
            revenue_data.append(float(day_sales))
            expense_data.append(float(day_expenses))
            
        context['chart_days'] = days
        context['chart_revenue'] = revenue_data
        context['chart_expenses'] = expense_data
        
        return context
