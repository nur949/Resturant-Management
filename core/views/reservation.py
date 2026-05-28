from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Reservation, Customer
from django.urls import reverse_lazy
from ..forms import ReservationForm, CustomerForm

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'core/reservation_list.html'
    context_object_name = 'reservations'
    ordering = ['date', 'time']

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('reservation_list')
    extra_context = {'title': 'Add Reservation'}

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('reservation_list')
    extra_context = {'title': 'Edit Reservation'}

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('reservation_list')

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'core/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('customer_list')
    extra_context = {'title': 'Add Customer'}

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('customer_list')
    extra_context = {'title': 'Edit Customer'}

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('customer_list')
