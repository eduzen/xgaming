import random
from decimal import Decimal

from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, MatchForm, DepositForm
from .forms import WithdrawnMoneyForm, WithdrawnBonusForm
from .models import Deposit, Wallet, BonusWallet


def withdrawnbonus(request):
    if request.method == 'POST':
        form = WithdrawnBonusForm(request.user, request.POST)
        if form.is_valid():
            withdrawn_bonus = form.save(commit=False)
            withdrawn_bonus.accepted = True
            return HttpResponse('Withdraw accepted')
        return HttpResponse('You need to play more!!!')

    return HttpResponseRedirect('home')


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.user, request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            wallet = Wallet.objects.filter(user=request.user)[0]
            deposit.wallet = wallet
            deposit.save()

    return HttpResponseRedirect('home')


def decide_match(form, user):
    """
        Save a match and decide if it wins or lose
    """
    match = form.save(commit=False)
    match.user = user
    # 1 or 0, just to have more chances to win
    match.result = random.randint(0, 1)
    if match.result:
        match.won = True

    match.save()
    return match.won

def process_payment(wallet, won):
    """
        Add or remove money from a Wallet
    """
    if won:
        wallet.value += Decimal('2.00')
    else:
        wallet.value -= Decimal('2.00')
    wallet.save()

def count_bonus_wagered(bonus_wallet):
    bonus_wallet.bet += Decimal('2.00')
    bonus_wallet.save()


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

        won = decide_match(form, request.user)
        if wallet.exists():
            process_payment(wallet[0], won)
        else:
            count_bonus_wagered(bonus_wallet[0])
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
        data['withdrawn_bonus'] = WithdrawnBonusForm(request.user)
        data['withdrawn_money'] = WithdrawnMoneyForm()
        data['deposit'] = DepositForm()
        w = Wallet.objects.filter(user=request.user).aggregate(Sum('value'))
        b = BonusWallet.objects.filter(user=request.user).aggregate(Sum('value'), Sum('bet'))
        data['money'] = w['value__sum']
        data['bonus'] = b['value__sum']
        data['wagered'] = b['bet__sum']

    return render(request, 'igaming/home.html', data)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
