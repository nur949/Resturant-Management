from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import Expense
from ..forms import ExpenseForm

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'core/expense_list.html'
    context_object_name = 'expenses'
    ordering = ['-date']

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('expense_list')
    extra_context = {'title': 'Add Expense'}

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('expense_list')
    extra_context = {'title': 'Edit Expense'}

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('expense_list')
