from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import Order, Table, MenuItem, Category

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'core/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

def create_order(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    order = Order.objects.create(table=table, staff=request.user)
    table.status = 'occupied'
    table.save()
    return redirect('order_detail', pk=order.id)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = MenuItem.objects.filter(is_available=True)
        context['categories'] = Category.objects.all()
        return context

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('order_list')

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        table = order.table
        table.status = 'available'
        table.save()
        return super().delete(request, *args, **kwargs)
