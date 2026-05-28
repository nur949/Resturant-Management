from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
        ('no-show', 'No Show'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey('Table', on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    guest_count = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reservation for {self.customer.name} at {self.date} {self.time}"
