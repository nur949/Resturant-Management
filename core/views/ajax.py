from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Order, MenuItem, OrderItem

def add_order_item(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        order = get_object_or_404(Order, id=order_id)
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        order_item, created = OrderItem.objects.get_or_create(
            order=order, 
            menu_item=menu_item,
            defaults={'price': menu_item.price, 'quantity': 0}
        )
        order_item.quantity += quantity
        order_item.save()
        
        return JsonResponse({
            'status': 'success',
            'item_name': menu_item.name,
            'quantity': order_item.quantity,
            'total_price': float(order.total_price)
        })
    return JsonResponse({'status': 'error'}, status=400)

def update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        payment_method = request.POST.get('payment_method', 'cash')
        tax_rate = request.POST.get('tax_rate', 0)

        order = get_object_or_404(Order, id=order_id)
        order.status = status
        
        if status == 'paid':
            order.payment_method = payment_method
            order.tax_rate = float(tax_rate)
            order.table.status = 'available'
            order.table.save()
            
            # Deduct inventory if recipes exist
            for item in order.items.all():
                recipe_items = item.menu_item.ingredients.all()
                for ri in recipe_items:
                    ri.ingredient.current_stock -= ri.quantity_required * item.quantity
                    ri.ingredient.save()
        
        order.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
