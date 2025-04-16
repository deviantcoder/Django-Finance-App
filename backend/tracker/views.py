from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Transaction
from .filters import TransactionFilter
from .forms import TransactionForm


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
    if request.htmx:
        print('>>> POST REQUEST INCOMING <<<')
        form = TransactionForm(request.POST)
        if form.is_valid():
            print('>>> POST REQUEST INCOMING <<<')
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            context = {'message': 'Transaction was added successfully'}

            return render(request, 'tracker/partials/transaction-success.html', context)

    context = {
        'form': TransactionForm(),
    }

    return render(request, 'tracker/partials/create-transaction.html', context)
