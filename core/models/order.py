from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cooking', 'Cooking'),
        ('served', 'Served'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Banking'),
    ]
    table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='orders')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # e.g. 5.00 for 5%
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table.number}"

    @property
    def invoice_number(self):
        return f"INV-{self.created_at.strftime('%Y%m')}-{self.id:05d}"

    @property
    def subtotal(self):
        return sum(item.get_total_item_price() for item in self.items.all())

    @property
    def tax_amount(self):
        return (self.subtotal * self.tax_rate) / 100

    @property
    def total_price(self):
        return self.subtotal + self.tax_amount
