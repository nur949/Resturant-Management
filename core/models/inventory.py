from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram (kg)'),
        ('ltr', 'Liter (ltr)'),
        ('pcs', 'Pieces (pcs)'),
        ('gm', 'Gram (gm)'),
        ('ml', 'Milliliter (ml)'),
    ]
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    current_stock = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    low_stock_threshold = models.DecimalField(max_digits=12, decimal_places=3, default=5)
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_restocked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.current_stock} {self.unit})"

    @property
    def stock_status(self):
        if self.current_stock <= 0:
            return 'out_of_stock'
        if self.current_stock <= self.low_stock_threshold:
            return 'low_stock'
        return 'in_stock'

class StockLog(models.Model):
    TYPE_CHOICES = [
        ('purchase', 'Purchase/Restock'),
        ('usage', 'Consumption (Order)'),
        ('adjustment', 'Manual Adjustment'),
        ('waste', 'Wastage'),
    ]
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    notes = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class RecipeItem(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_required = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f"{self.quantity_required} {self.ingredient.unit} of {self.ingredient.name} for {self.menu_item.name}"
