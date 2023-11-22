from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import WalletForm
from .models import Transaction, Wallet


def user_wallet(request):
    user_wallet = Wallet.objects.get(user=request.user)
    user_transactions = Transaction.objects.filter(user=request.user)
    context = {
        "user_wallet": user_wallet,
        "user_transactions": user_transactions,
    }
    return render(request, "wallet/user_wallet.html", context)


def deposit_view(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            user_wallet = Wallet.objects.get(user=request.user)
            user_wallet.balance += amount
            user_wallet.save()
            Transaction.objects.create(
                user=request.user,
                transaction_type=Transaction.TransactionTypes.DEPOSIT,
                amount=amount,
            )
            messages.success(request, f"${amount} is deposited to your wallet")
            return redirect("wallet:user_wallet")
    else:
        form = WalletForm()

    context = {"form": form}
    return render(request, "wallet/deposit.html", context)


def withdraw_view(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            user_wallet = Wallet.objects.get(user=request.user)
            if user_wallet.balance >= amount:
                user_wallet.balance -= amount
                user_wallet.save()
                Transaction.objects.create(
                    user=request.user,
                    transaction_type=Transaction.TransactionTypes.WITHDRAW,
                    amount=amount,
                )
                messages.success(request, f"${amount} is credited from your wallet")
                return redirect("wallet:user_wallet")
            else:
                messages.error(request, "Insufficient balance")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = WalletForm()

    context = {"form": form}
    return render(request, "wallet/withdraw.html", context)


def clear_transactions_history(request):
    user_transactions = Transaction.objects.filter(user=request.user)
    user_transactions.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
