from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

from .models import User


@require_http_methods(['POST', 'GET'])
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

@require_http_methods(['POST', 'GET'])
def login_view(request):
    # GET request for when the user navigates to this page in the browser
    if request.method == 'GET':
        return render(request, 'user/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user: User | None = authenticate(request, username=username, password=password)
    if user is None:
        messages.error(request, 'Invalid username or password.')

    login(request, user)
    messages.success(request, 'Login successful!')

    dashboard_url = 'dashboard'
    if user.role == User.Roles.SELLER:
        dashboard_url = 'seller_dashboard'

    return redirect(dashboard_url)


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'user/dashboard.html')
