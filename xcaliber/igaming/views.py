import random
from decimal import Decimal

from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, MatchForm, DepositForm, WithdrawnForm
from .models import Deposit, Wallet, BonusWallet


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            wallet = Wallet.objects.filter(user=request.user)
            if wallet.exists():
                deposit.wallet = wallet[0]
            deposit.save()

    return HttpResponseRedirect('home')


def decide_match(form, user):
    match = form.save(commit=False)
    match.user = user
    # 1 or 0, just to have more chances to win
    match.result = random.randint(0, 1)
    if match.result:
        match.won = True

    match.save()
    return match.won

def process_payment(wallet, won):
    if won:
        wallet.value += Decimal('2.00')
    else:
        wallet.value -= Decimal('2.00')
    wallet.save()


@login_required
def play(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Something went wrong!")

        wallet = Wallet.objects.filter(user=request.user, value__gt=Decimal('2.00'))
        bonus_wallet = BonusWallet.objects.filter(user=request.user, value__gt=Decimal('2.00'))
        if not wallet.exists() and not bonus_wallet.exists():
            return HttpResponse("You need money!")

        won = decide_match(form, user)

        if wallet.exists():
            process_payment(wallet[0], won)
        else:
            process_payment(bonus_wallet[0], won)

        return HttpResponseRedirect("home")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('home')
    else:
        form = SignUpForm()
    return render(request, 'igaming/signup.html', {'form': form})


def home(request):
    data = {}
    if request.user.is_authenticated:
        data['form'] = MatchForm()
        data['withdrawn'] = WithdrawnForm()
        data['deposit'] = DepositForm()
        w = Wallet.objects.filter(user=request.user).aggregate(Sum('value'))
        b = BonusWallet.objects.filter(user=request.user).aggregate(Sum('value'))
        data['money'] = w['value__sum']
        data['bonus'] = b['value__sum']

    return render(request, 'igaming/home.html', data)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
