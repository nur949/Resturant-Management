from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import AuditLog

class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'core/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 50
