from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import CustomSetPasswordForm, CustomPasswordResetForm

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

User = get_user_model()
# Reset
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = '/accounts/reset/password/done/'
    email_template_name = 'accounts/custom_password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        associated_users = User.objects.filter(email=email)
        if not associated_users.exists():
            messages.error(self.request, 'Email address is not registered.')
            return self.form_invalid(form)
        return super().form_valid(form)
    

# Reset Confirmasi
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'

    def form_invalid(self, form):
        messages.error(self.request, "Password yang dimasukkan tidak sesuai. Silakan periksa kembali.")
        return super().form_invalid(form)
    
    def dispatch(self, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            self.validlink = True
        else:
            self.validlink = False

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = self.validlink
        return context

def login_view(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    if user.is_admin:
                        auth_login(request, user)
                        return redirect('dashboard_admin')
                    elif user.is_staff:
                        auth_login(request, user)
                        return redirect('dashboard_staff')
                    elif hasattr(user, 'is_pelanggan') and user.is_pelanggan:
                        auth_login(request, user)
                        return redirect('dashboard_pelanggan')
                    else:
                        messages.error(request, 'User type is not recognized.')
                else:
                    messages.error(request, 'Account is inactive.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Error validating form.')
    
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to your desired page after signup
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

# Logout View

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html') 

@login_required
def dashboard(request):
    # Mengambil nama pengguna dari request.user
    user_name = request.user.first_name or request.user.username
    context = {
        'user_name': user_name,
    }
    return render(request, 'dashboard.html', context) 

@login_required
def dashboard_pelanggan(request):
    # Mengambil nama pengguna dari request.user
    user_name = request.user.first_name or request.user.username
    context = {
        'user_name': user_name,
    }
    return render(request, 'dashboard/pelanggan.html', context)
