from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
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

from .middleware import get_current_user

def log_action(instance, action):
    user = get_current_user()
    if user and not user.is_authenticated:
        user = None
        
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

@receiver(post_save, sender=Reservation)
def update_table_status_on_reservation(sender, instance, **kwargs):
    table = instance.table
    if instance.status == 'confirmed':
        table.status = 'reserved'
    elif instance.status == 'arrived':
        table.status = 'occupied'
    elif instance.status in ['cancelled', 'no-show']:
        table.status = 'available'
    table.save()

@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    if sender in [User, Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation]:
        action = 'create' if created else 'update'
        log_action(instance, action)

@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if sender in [User, Category, MenuItem, Table, Order, OrderItem, Expense, Ingredient, RecipeItem, Customer, Reservation]:
        log_action(instance, 'delete')
