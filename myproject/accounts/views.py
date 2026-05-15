from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(request, 'accounts/login.html', {
                'error': 'Username and password are required'
            })

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('profile')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password. Please check and try again.'
            })

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        email = request.POST.get('email', '').strip()

        # Validation
        if not username or not password or not confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'All fields are required',
                'username': username,
                'email': email
            })

        if len(username) < 3:
            return render(request, 'accounts/register.html', {
                'error': 'Username must be at least 3 characters long',
                'username': username,
                'email': email
            })

        if len(password) < 6:
            return render(request, 'accounts/register.html', {
                'error': 'Password must be at least 6 characters long',
                'username': username,
                'email': email
            })

        if password != confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match',
                'username': username,
                'email': email
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists',
                'email': email
            })

        if email and User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Email already registered',
                'username': username
            })

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        except Exception as e:
            return render(request, 'accounts/register.html', {
                'error': f'Error creating account: {str(e)}',
                'username': username,
                'email': email
            })

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })