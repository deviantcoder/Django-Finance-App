from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Transaction
from .filters import TransactionFilter
from .forms import TransactionForm

from django_htmx.http import retarget


def index(request):
    return render(request, 'tracker/index.html')


@login_required
def transactions_list(request):
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    total_income = transactions_filter.qs.get_total_income()
    total_expenses = transactions_filter.qs.get_total_expenses()

    context = {
        'filter': transactions_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses,
    }

    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)

    return render(request, 'tracker/transactions-list.html', context)


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            context = {'message': 'Transaction was added successfully'}

            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
            }
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')

    context = {
        'form': TransactionForm(),
    }

    return render(request, 'tracker/partials/create-transaction.html', context)


@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()

            context = {
                'message': 'Transaction was updated successfully'
            }

            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
                'transaction': transaction,
            }
            response = render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')  

    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction,
    }

    return render(request, 'tracker/partials/update-transaction.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()

    context = {
        'message': f'Transaction of {transaction.amount} on {transaction.date} was deleted!'
    }

    return render(request, 'tracker/partials/transaction-success.html', context)
