from django.views.generic import CreateView, UpdateView, DeleteView
from .authforms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class CreateAccountView(CreateView):
    form_class = CustomCreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

class LoginAccountView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy("dashboard")
    redirect_authenticated_user = True

class CHPasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy("account")

class PWDResetView(PasswordResetView):
    
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy("login")

class EDAccountView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/edit_account.html'
    success_url = reverse_lazy("account")

    def get_object(self):
        return self.request.user

class DLAccountView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'registration/delete_user_confirm.html'
    success_message = "User Deleted Successfully"
    success_url = reverse_lazy("index")

    def get_object(self):
        return self.request.user
    

def log_out(request):
    logout(request)
    return redirect("index")