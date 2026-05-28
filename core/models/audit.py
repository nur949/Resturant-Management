from django.db import models
from django.contrib.auth.models import User
import json

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    object_repr = models.CharField(max_length=255) # String representation of the object
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(blank=True, null=True) # JSON snapshot of changes

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        return f"{self.user} {self.action} {self.model_name}: {self.object_repr}"

    # Pro-level protection: Prevent deletion and updates via model methods
    def delete(self, *args, **kwargs):
        raise Exception("Audit Logs are permanent and cannot be deleted.")

    def save(self, *args, **kwargs):
        if self.pk:
            raise Exception("Audit Logs are immutable and cannot be modified.")
        super().save(*args, **kwargs)
