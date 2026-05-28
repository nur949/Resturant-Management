from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import Table
from ..forms import TableForm

class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'core/table_list.html'
    context_object_name = 'tables'

class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('table_list')
    extra_context = {'title': 'Add Table'}

class TableUpdateView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('table_list')
    extra_context = {'title': 'Edit Table'}

class TableDeleteView(LoginRequiredMixin, DeleteView):
    model = Table
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('table_list')
