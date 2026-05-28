from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import models
from ..models import Ingredient, StockLog
from ..forms import IngredientForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'core/inventory/ingredient_list.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['low_stock_count'] = Ingredient.objects.filter(current_stock__lte=models.F('low_stock_threshold')).count()
        context['total_inventory_value'] = sum(i.current_stock * i.cost_per_unit for i in Ingredient.objects.all())
        return context

class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = 'core/inventory/ingredient_detail.html'
    context_object_name = 'ingredient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock_logs'] = self.object.logs.all()[:20]
        return context

# CRUD Views
class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('ingredient_list')
    extra_context = {'title': 'Add New Ingredient'}

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('ingredient_list')
    extra_context = {'title': 'Edit Ingredient'}

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('ingredient_list')

# Enterprise Stock Operations
def update_stock(request, pk):
    if request.method == 'POST':
        ingredient = get_object_or_404(Ingredient, pk=pk)
        amount = float(request.POST.get('amount', 0))
        action_type = request.POST.get('action_type') # 'purchase', 'adjustment', 'waste'
        notes = request.POST.get('notes', '')
        
        if action_type == 'purchase':
            ingredient.current_stock += amount
        elif action_type in ['waste', 'usage']:
            ingredient.current_stock -= amount
        else: # adjustment
             ingredient.current_stock = amount # Direct set for adjustment
            
        ingredient.save()
        
        # Create enterprise ledger log
        StockLog.objects.create(
            ingredient=ingredient,
            user=request.user,
            type=action_type,
            quantity=amount,
            notes=notes
        )
        
        messages.success(request, f"Inventory ledger updated for {ingredient.name}")
        return redirect('ingredient_list')
