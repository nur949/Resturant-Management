from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation, AuditLog
import json
import decimal
from datetime import date, datetime

# Helper to handle non-serializable types in JSON
class DjangoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (decimal.Decimal, date, datetime)):
            return str(obj)
        return super().default(obj)

def get_current_user():
    # Since signals don't natively have access to the request/user,
    # we would typically use a middleware to store the current user in thread local storage.
    # For this implementation, we'll assume a simplified approach or leave it for the middleware.
    return None 

def log_action(instance, action, user=None):
    model_name = instance.__class__.__name__
    if model_name == 'AuditLog':
        return

    try:
        changes = json.dumps(model_to_dict(instance), cls=DjangoJSONEncoder)
    except:
        changes = "{}"

    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=instance.id,
        object_repr=str(instance),
        changes=changes
    )

@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    if sender in [Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation]:
        action = 'create' if created else 'update'
        log_action(instance, action)

@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if sender in [Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation]:
        log_action(instance, 'delete')
