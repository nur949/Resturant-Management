from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from ..models import Order, MenuItem, OrderItem

from django.contrib.auth.models import User

def toggle_user_status(request):
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        if user != request.user: # Prevents deactivating self
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({'status': 'success', 'is_active': user.is_active})
    return JsonResponse({'status': 'error'}, status=400)

import secrets
import string

def reset_user_password(request):
    if request.method == 'POST' and request.user.is_superuser:
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # Generate a secure random password
        alphabet = string.ascii_letters + string.digits + string.punctuation
        temp_password = ''.join(secrets.choice(alphabet) for i in range(12))
        
        user.set_password(temp_password)
        user.save()
        return JsonResponse({'status': 'success', 'message': f'Password reset to: {temp_password}'})
    return JsonResponse({'status': 'error'}, status=400)

def add_order_item(request):
    try:
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            item_id = request.POST.get('item_id')
            quantity = int(request.POST.get('quantity', 1))
            
            print(f"DEBUG: Adding item {item_id} to order {order_id}")
            
            order = get_object_or_404(Order, id=order_id)
            menu_item = get_object_or_404(MenuItem, id=item_id)
            
            order_item, created = OrderItem.objects.get_or_create(
                order=order, 
                menu_item=menu_item,
                defaults={'price': menu_item.price, 'quantity': 0}
            )
            order_item.quantity += quantity
            order_item.save()
            
            print(f"DEBUG: Item added. Current count for item: {order_item.quantity}")
            return get_cart_details_json(order)
    except Exception as e:
        print(f"ERROR in add_order_item: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def update_cart_item(request):
    try:
        if request.method == 'POST':
            order_item_id = request.POST.get('order_item_id')
            action = request.POST.get('action')
            
            order_item = get_object_or_404(OrderItem, id=order_item_id)
            order = order_item.order
            
            if action == 'add':
                order_item.quantity += 1
                order_item.save()
            elif action == 'subtract':
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                else:
                    order_item.delete()
            elif action == 'remove':
                order_item.delete()
                
            return get_cart_details_json(order)
    except Exception as e:
        print(f"ERROR in update_cart_item: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=400)

def get_cart_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return get_cart_details_json(order)

def get_cart_details_json(order):
    items_data = []
    for item in order.items.all():
        items_data.append({
            'id': item.id,
            'name': item.menu_item.name,
            'quantity': item.quantity,
            'price': float(item.price),
            'total': float(item.get_total_item_price())
        })
    
    return JsonResponse({
        'status': 'success',
        'items': items_data,
        'subtotal': float(order.subtotal),
        'tax_amount': float(order.tax_amount),
        'total_price': float(order.total_price),
        'item_count': order.items.count()
    })

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
