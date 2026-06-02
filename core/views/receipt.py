from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from ..models import Order

class ReceiptDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/receipt_print.html'
    context_object_name = 'order'
