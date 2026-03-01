from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import EnergyListing
from .forms import EnergyListingForm


def listing_list(request):
    """View all energy listings"""
    listings = EnergyListing.objects.filter(status='active')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(energy_type__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by energy type
    energy_type = request.GET.get('energy_type')
    if energy_type:
        listings = listings.filter(energy_type=energy_type)

    context = {
        'listings': listings,
        'search_query': search_query,
        'energy_type': energy_type,
    }
    return render(request, 'marketplace/listing_list.html', context)


def listing_detail(request, pk):
    """View single listing details"""
    listing = get_object_or_404(EnergyListing, pk=pk)
    return render(request, 'marketplace/listing_detail.html', {'listing': listing})


@login_required
def create_listing(request):
    """Create new energy listing (Producer only)"""
    if request.user.role != 'producer':
        messages.error(request, 'Only producers can create listings.')
        return redirect('marketplace:listing_list')

    if request.method == 'POST':
        form = EnergyListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.producer = request.user

            # Get energy type from producer profile
            try:
                listing.energy_type = request.user.producer_profile.energy_type
            except:
                messages.error(request, 'Please complete your producer profile first.')
                return redirect('accounts:complete_profile')

            listing.save()
            messages.success(request, 'Energy listing created successfully!')
            return redirect('marketplace:listing_detail', pk=listing.pk)
    else:
        form = EnergyListingForm()

    return render(request, 'marketplace/create_listing.html', {'form': form})


@login_required
def my_listings(request):
    """View producer's own listings"""
    if request.user.role != 'producer':
        messages.error(request, 'Only producers can view listings.')
        return redirect('marketplace:listing_list')

    listings = EnergyListing.objects.filter(producer=request.user)
    return render(request, 'marketplace/my_listings.html', {'listings': listings})


@login_required
def update_listing(request, pk):
    """Update existing listing"""
    listing = get_object_or_404(EnergyListing, pk=pk, producer=request.user)

    if request.method == 'POST':
        form = EnergyListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('marketplace:listing_detail', pk=listing.pk)
    else:
        form = EnergyListingForm(instance=listing)

    return render(request, 'marketplace/create_listing.html', {'form': form, 'listing': listing})


@login_required
def delete_listing(request, pk):
    """Delete listing"""
    listing = get_object_or_404(EnergyListing, pk=pk, producer=request.user)
    listing.delete()
    messages.success(request, 'Listing deleted successfully!')
    return redirect('marketplace:my_listings')