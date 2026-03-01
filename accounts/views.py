from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import UserRegistrationForm, ProducerProfileForm, ConsumerProfileForm, InvestorProfileForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('accounts:complete_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def complete_profile(request):
    user = request.user

    if user.role == 'producer':
        form_class = ProducerProfileForm
        profile_attr = 'producer_profile'
    elif user.role == 'consumer':
        form_class = ConsumerProfileForm
        profile_attr = 'consumer_profile'
    elif user.role == 'investor':
        form_class = InvestorProfileForm
        profile_attr = 'investor_profile'
    else:
        messages.error(request, 'Invalid user role')
        return redirect('home')

    # Check if profile already exists
    try:
        profile = getattr(user, profile_attr)
        instance = profile
    except:
        instance = None

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Profile completed successfully!')
            return redirect('accounts:dashboard')
    else:
        form = form_class(instance=instance)

    return render(request, 'accounts/complete_profile.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}

    if user.role == 'producer':
        try:
            profile = user.producer_profile
            context['profile'] = profile
            # Get producer's listings
            from marketplace.models import EnergyListing
            context['listings'] = EnergyListing.objects.filter(producer=user)
        except:
            messages.warning(request, 'Please complete your producer profile first.')
            return redirect('accounts:complete_profile')

    elif user.role == 'consumer':
        try:
            profile = user.consumer_profile
            context['profile'] = profile
            # Get consumer's orders
            from transactions.models import Order
            context['orders'] = Order.objects.filter(consumer=user)[:5]
        except:
            messages.warning(request, 'Please complete your consumer profile first.')
            return redirect('accounts:complete_profile')

    elif user.role == 'investor':
        try:
            profile = user.investor_profile
            context['profile'] = profile
            # Get investor's investments
            from investments.models import Investment
            context['investments'] = Investment.objects.filter(investor=user)
        except:
            messages.warning(request, 'Please complete your investor profile first.')
            return redirect('accounts:complete_profile')

    return render(request, 'accounts/dashboard.html', context)