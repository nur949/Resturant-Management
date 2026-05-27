from .models import Ingredient

def low_stock_processor(request):
    if request.user.is_authenticated:
        # We need to compute this safely. 
        # For performance, maybe just a count.
        low_stock_count = 0
        ingredients = Ingredient.objects.all()
        for item in ingredients:
            if item.current_stock <= item.low_stock_threshold:
                low_stock_count += 1
        return {'sidebar_low_stock_count': low_stock_count}
    return {'sidebar_low_stock_count': 0}
