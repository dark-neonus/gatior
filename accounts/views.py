# accounts/views.py

from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm

class RegisterView(CreateView):
    """
    View to handle user registration.
    """
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("blog:feed")

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)  # Correctly log in the user
        return super().form_valid(form)
    
class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("blog:feed")

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("blog:feed"))
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})
    

def logout_view(request):
    logout(request)
    return redirect(reverse_lazy("auth:login"))