from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction
from decimal import Decimal

from .models import InvestmentProject, Investment
from transactions.models import Transaction   # ✅ IMPORTANT


def projects_list(request):
    """View all investment projects"""

    projects = InvestmentProject.objects.filter(status__in=['funding', 'active'])

    energy_type = request.GET.get('energy_type')
    if energy_type:
        projects = projects.filter(energy_type=energy_type)

    return render(request, 'projects_list.html', {'projects': projects})


def project_detail(request, pk):
    """View project details"""

    project = get_object_or_404(InvestmentProject, pk=pk)
    investments = project.investments.all()[:5]

    context = {
        'project': project,
        'investments': investments,
        'total_investors': project.investments.count()
    }

    return render(request, 'project_detail.html', context)


@login_required
def invest(request, project_id):
    """Invest in a project"""

    if request.user.role != 'investor':
        messages.error(request, 'Only investors can invest in projects.')
        return redirect('investments:projects_list')

    project = get_object_or_404(InvestmentProject, pk=project_id)

    if project.status != 'funding':
        messages.error(request, 'This project is not accepting investments.')
        return redirect('investments:project_detail', pk=project_id)

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))

            if amount <= 0:
                messages.error(request, 'Investment amount must be greater than 0.')
                return redirect('investments:project_detail', pk=project_id)

            # Check investor profile
            try:
                investor_profile = request.user.investor_profile
            except:
                messages.error(request, 'Please complete your investor profile first.')
                return redirect('complete_profile')

            if amount > investor_profile.investment_capacity:
                messages.error(request, 'Investment amount exceeds your capacity.')
                return redirect('investments:project_detail', pk=project_id)

            remaining = project.total_funding_required - project.funding_raised

            if amount > remaining:
                messages.error(request, f'Project only needs ₹{remaining} more funding.')
                return redirect('investments:project_detail', pk=project_id)

            # ✅ ATOMIC TRANSACTION (SAFE)
            with transaction.atomic():

                # Create Investment
                investment = Investment.objects.create(
                    project=project,
                    investor=request.user,
                    amount=amount
                )

                # ✅ CREATE TRANSACTION RECORD
                Transaction.objects.create(
                    order=None,
                    transaction_type='investment',
                    amount=amount,
                    from_user=request.user,        # Investor
                    to_user=project.owner,         # Project Owner / Producer
                    payment_gateway='UPI',
                    is_successful=True
                )

                # Update funding
                project.funding_raised += amount

                if project.funding_raised >= project.total_funding_required:
                    project.status = 'active'

                project.save()

            messages.success(
                request,
                f'Successfully invested ₹{amount} in {project.title}!'
            )

            return redirect('investments:my_investments')

        except Exception:
            messages.error(request, 'Invalid amount entered.')
            return redirect('investments:project_detail', pk=project_id)

    return render(request, 'investments/invest.html', {'project': project})


@login_required
def my_investments(request):
    """View investor's investments"""

    if request.user.role != 'investor':
        messages.error(request, 'Only investors can view investments.')
        return redirect('home')

    investments = Investment.objects.filter(investor=request.user)

    total_invested = investments.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    total_expected_return = investments.aggregate(
        total=Sum('expected_return')
    )['total'] or Decimal('0')

    total_actual_return = investments.aggregate(
        total=Sum('actual_return')
    )['total'] or Decimal('0')

    context = {
        'investments': investments,
        'total_invested': total_invested,
        'total_expected_return': total_expected_return,
        'total_actual_return': total_actual_return,
    }

    return render(request, 'my_investments.html', context)


@login_required
def investor_dashboard(request):
    """Investor dashboard"""

    if request.user.role != 'investor':
        messages.error(request, 'Only investors can access this page.')
        return redirect('home')

    investments = Investment.objects.filter(investor=request.user)

    total_invested = investments.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0')

    context = {
        'total_investments': investments.count(),
        'total_invested': total_invested,
        'active_investments': investments.filter(status='active').count(),
        'recent_investments': investments.order_by('-id')[:5],
    }

    return render(request, 'investor_dashboard.html', context)