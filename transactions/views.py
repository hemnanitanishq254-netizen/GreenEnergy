from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, Transaction
from marketplace.models import EnergyListing


@login_required
def create_order(request, listing_id):
    """Create order for energy purchase"""

    if request.user.role != 'consumer':
        messages.error(request, 'Only consumers can purchase energy.')
        return redirect('marketplace:listing_list')

    listing = get_object_or_404(EnergyListing, pk=listing_id, status='active')

    if request.method == 'POST':
        try:
            quantity = float(request.POST.get('quantity_kwh'))

            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0.')
                return redirect('transactions:create_order', listing_id=listing_id)

            if quantity > float(listing.quantity_kwh):
                messages.error(request, 'Requested quantity exceeds available energy.')
                return redirect('marketplace:listing_detail', pk=listing_id)

            order = Order.objects.create(
                consumer=request.user,
                listing=listing,
                quantity_kwh=quantity,
                total_amount=quantity * float(listing.price_per_kwh),
                status='pending'
            )

            messages.success(request, 'Order created successfully! Proceed to payment.')
            return redirect('transactions:payment', order_id=order.id)

        except (TypeError, ValueError):
            messages.error(request, 'Invalid quantity entered.')
            return redirect('transactions:create_order', listing_id=listing_id)

    return render(request, 'create_order.html', {'listing': listing})


@login_required
def payment(request, order_id):
    """Payment page"""

    order = get_object_or_404(Order, pk=order_id, consumer=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        with transaction.atomic():

            # Update order
            order.status = 'confirmed'
            order.payment_method = payment_method
            order.transaction_id = f"TXN{order.id}{order.created_at.strftime('%Y%m%d%H%M%S')}"
            order.save()

            # Create transaction record
            Transaction.objects.create(
                order=order,
                transaction_type='purchase',
                amount=order.total_amount,
                from_user=request.user,
                to_user=order.listing.producer,
                payment_gateway=payment_method,
                is_successful=True
            )

            # Reduce listing quantity
            listing = order.listing
            listing.quantity_kwh -= order.quantity_kwh

            if listing.quantity_kwh <= 0:
                listing.status = 'sold'

            listing.save()

        messages.success(request, 'Payment successful! Your order has been confirmed.')
        return redirect('transactions:order_detail', order_id=order.id)

    return render(request, 'payment.html', {'order': order})


@login_required
def order_detail(request, order_id):
    """View order details"""

    order = get_object_or_404(Order, pk=order_id)

    if order.consumer != request.user and order.listing.producer != request.user:
        messages.error(request, 'You are not authorized to view this order.')
        return redirect('accounts:dashboard')

    return render(request, 'order_detail.html', {'order': order})


@login_required
def my_orders(request):
    """View user's orders"""

    if request.user.role == 'consumer':
        orders = Order.objects.filter(consumer=request.user).order_by('-created_at')
        title = "My Purchases"

    elif request.user.role == 'producer':
        orders = Order.objects.filter(listing__producer=request.user).order_by('-created_at')
        title = "My Sales"

    else:
        messages.error(request, 'Invalid user role.')
        return redirect('home')

    return render(request, 'my_orders.html', {
        'orders': orders,
        'title': title
    })


@login_required
def transaction_history(request):
    """View transaction history"""

    if request.user.role == 'consumer':
        transactions_list = Transaction.objects.filter(
            from_user=request.user,
            is_successful=True
        ).order_by('-id')

    elif request.user.role == 'producer':
        transactions_list = Transaction.objects.filter(
            to_user=request.user,
            is_successful=True
        ).order_by('-id')

    else:
        messages.error(request, 'Invalid user role.')
        return redirect('home')

    return render(request, 'transactions/transaction_history.html', {
        'transactions': transactions_list
    })