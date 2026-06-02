from django.db import models

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('served', 'Served'),
    ]
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at the time of order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    def get_total_item_price(self):
        return self.quantity * self.price
