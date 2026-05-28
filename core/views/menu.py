from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models import MenuItem, Category
from ..forms import MenuItemForm, CategoryForm

class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'core/menu_list.html'
    context_object_name = 'menu_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# Category CRUD
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('menu_list')
    extra_context = {'title': 'Add Category'}

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('menu_list')
    extra_context = {'title': 'Edit Category'}

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('menu_list')

# MenuItem CRUD
class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('menu_list')
    extra_context = {'title': 'Add Menu Item'}

class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('menu_list')
    extra_context = {'title': 'Edit Menu Item'}

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('menu_list')
