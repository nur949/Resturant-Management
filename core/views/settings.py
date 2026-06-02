from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from ..models import RestaurantSetting
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from ..forms import RestaurantSettingForm, UserForm, UserAccountForm, PersonalProfileForm

class PersonalProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/settings/personal_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account_form'] = UserAccountForm(instance=self.request.user)
        context['profile_form'] = PersonalProfileForm(instance=self.request.user.profile)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        
        if action == 'update_account':
            account_form = UserAccountForm(request.POST, instance=request.user)
            profile_form = PersonalProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if account_form.is_valid() and profile_form.is_valid():
                account_form.save()
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
            return redirect('personal_profile')
            
        elif action == 'change_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user) # Keep user logged in
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Error updating password. Please check the details.")
            return redirect('personal_profile')
            
        return self.get(request, *args, **kwargs)

class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class SettingsView(LoginRequiredMixin, AdminOnlyMixin, TemplateView):
    template_name = 'core/settings/settings_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = RestaurantSetting.load()
        context['users'] = User.objects.all()
        return context

class RestaurantSettingUpdateView(LoginRequiredMixin, AdminOnlyMixin, UpdateView):
    model = RestaurantSetting
    form_class = RestaurantSettingForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('settings_home')
    extra_context = {'title': 'Update Restaurant Settings'}

    def get_object(self):
        return RestaurantSetting.load()

# User Management
class UserListView(LoginRequiredMixin, AdminOnlyMixin, ListView):
    model = User
    template_name = 'core/settings/user_list.html'
    context_object_name = 'users'

class UserCreateView(LoginRequiredMixin, AdminOnlyMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('settings_home')
    extra_context = {'title': 'Add New Staff Member'}

class UserUpdateView(LoginRequiredMixin, AdminOnlyMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('settings_home')
    extra_context = {'title': 'Edit Staff Member'}

class UserDeleteView(LoginRequiredMixin, AdminOnlyMixin, DeleteView):
    model = User
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('settings_home')
