from django.shortcuts import redirect,render
from . import forms
from .models import UserModel
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    success_url = reverse_lazy("login")
    form_class = forms.RegistrationForm
    success_message = "Check your email to confirmation."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = f"http://127.0.0.1:8000/users/activate/{uid}/{token}"
        print("uid -> ",uid)
        print("token -> ",token)
        email_subject = 'Confirm Your Email'
        email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})

        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        messages.success(self.request, self.success_message)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Signup"
        return context

class ActivateAccountView(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print(user)
        print("uid64 --> ",uid64)
        print("token --> ", token)
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return redirect('signup')
        
class UserLoginView(LoginView):
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("login")

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