from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Order
from django import forms
# Create your views here.

def signup(request):
    if request.method == 'POST':
        # Handle both 'name'/'full_name' and 'first_name'/'last_name' for flexibility
        first_name = request.POST.get('name') or request.POST.get('first_name', '')
        last_name = request.POST.get('full_name') or request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validate required fields
        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'accounts/signup.html')
        
        # Validate password confirmation if provided, otherwise skip
        if confirm_password and password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accounts/signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use')
            return render(request, 'accounts/signup.html')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=email, 
                password=password, 
                email=email, 
                first_name=first_name, 
                last_name=last_name
            )
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'accounts/signup.html')
    
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')  #redirect to homepage
        else:
            messages.error(request, 'Email or password incorrect')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

@login_required
def my_account(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')[:10]
    return render(request, 'accounts/my_account.html', {
        'user_obj': user,
        'orders': orders,
    })

@login_required
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password:
            if password == confirm_password:
                user.set_password(password)
            else:
                messages.error(request, 'Passwords do not match')
                return render(request, 'accounts/edit_account.html', {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                })

        user.save()
        messages.success(request, 'Your account has been updated successfully.')
        return redirect('my_account')

    return render(request, 'accounts/edit_account.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })
