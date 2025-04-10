from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Transaction
from .filters import TransactionFilter


def index(request):
    return render(request, 'tracker/index.html')


@login_required
def transactions_list(request):
    transactions_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user)
    )

    context = {
        'filter': transactions_filter,
    }

    return render(request, 'tracker/transactions-list.html', context)
