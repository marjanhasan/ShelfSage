from django.shortcuts import render
from . import forms
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist
from transactions.models import Transaction

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    success_url = reverse_lazy("login")
    form_class = forms.RegistrationForm
    success_message = "Your account created successfully."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Signup"
        return context

        
class UserLoginView(LoginView):
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "You are successfully logged in")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Email/Password is incorrect")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login"
        return context


@method_decorator(login_required, name="dispatch")
class UserLogoutView(LogoutView):
    template_name = "logout.html"

    def get_success_url(self):
        return reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, "Logged out successfully!")
        return response
    


@login_required
def profile_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    transaction_history = Transaction.objects.filter(user=request.user)

    return render(request, 'profile.html', {'wishlist_items': wishlist_items,'transaction_history': transaction_history})
