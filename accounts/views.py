import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Account
from .forms import TransferForm
import uuid

def import_accounts(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Account.objects.create(
                id=uuid.UUID(row['ID']),
                name=row['Name'],
                balance=row['Balance']
            )
        return redirect('list_accounts')
    return render(request, 'accounts/import_accounts.html')

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'accounts/list_accounts.html', {'accounts': accounts})

def account_info(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    return JsonResponse({'name': account.name, 'balance': account.balance})

def transfer_funds(request):
    error_message = None
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                return redirect('list_accounts')
            else:
                error_message = 'Insufficient funds'
    else:
        form = TransferForm()
    return render(request, 'accounts/transfer_funds.html', {'form': form, 'error_message': error_message})
