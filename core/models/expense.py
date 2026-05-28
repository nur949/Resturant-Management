from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('utility', 'Utility Bill'),
        ('salary', 'Staff Salary'),
        ('supply', 'Kitchen Supplies'),
        ('rent', 'Rent'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_category_display()} - {self.amount}"
