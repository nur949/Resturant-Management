from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Order, OrderItem
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class KitchenDashboardView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/kitchen_dashboard.html'
    context_object_name = 'active_orders'

    def get_queryset(self):
        # Only show orders that are not paid or cancelled and have items not yet served
        return Order.objects.filter(
            status__in=['pending', 'cooking', 'served']
        ).exclude(status='paid').order_by('created_at')

def get_active_orders_json(request):
    active_orders = Order.objects.filter(
        status__in=['pending', 'cooking', 'served']
    ).exclude(status='paid').order_by('created_at')
    
    orders_data = []
    for order in active_orders:
        items = []
        for item in order.items.all():
            items.append({
                'id': item.id,
                'name': item.menu_item.name,
                'quantity': item.quantity,
                'status': item.status,
            })
        
        orders_data.append({
            'id': order.id,
            'table_number': order.table.number,
            'created_at': order.created_at.isoformat(),
            'status': order.get_status_display(),
            'staff': order.staff.username if order.staff else 'System',
            'items': items
        })
    
    return JsonResponse({'status': 'success', 'orders': orders_data})

def update_item_status(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_status = request.POST.get('status')
        item = get_object_or_404(OrderItem, id=item_id)
        item.status = new_status
        item.save()
        
        # Check if all items in the order are ready/served to update the overall order status
        order = item.order
        if all(i.status in ['ready', 'served'] for i in order.items.all()):
            if order.status == 'pending':
                order.status = 'cooking' # Or 'ready' depending on workflow
                order.save()
                
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
