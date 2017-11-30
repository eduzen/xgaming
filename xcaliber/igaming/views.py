import random
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.edit import FormView

from config.models import WageringRequirement

from .forms import (DepositForm, MatchForm, SignUpForm, WithdrawnBonusForm,
                    WithdrawnMoneyForm)
from .models import BonusWallet, Wallet


class PlayView(View):

    @method_decorator(login_required)
    def post(self, request):
        form = MatchForm(request.POST)
        if not form.is_valid():
            return HttpResponse("Something went wrong!")

        wallet = Wallet.objects.filter(
            user=request.user, value__gt=Decimal('2.00')
        )
        bonus_wallet = BonusWallet.objects.filter(
            user=request.user, value__gt=Decimal('2.00')
        )
        if not wallet.exists() and not bonus_wallet.exists():
            return HttpResponse("You need money!")

        won = self._decide_match(form, request.user)
        if wallet.exists():
            self._process_payment(wallet[0], won)
        else:
            self._count_bonus_wagered(bonus_wallet[0])
            self._process_payment(bonus_wallet[0], won)

        return HttpResponseRedirect("home")

    def _decide_match(self, form, user):
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

    def _process_payment(self, wallet, won):
        """
            Add or remove money from a Wallet
        """
        if won:
            wallet.value += Decimal('2.00')
        else:
            wallet.value -= Decimal('2.00')
        wallet.save()

    def _count_bonus_wagered(self, bonus_wallet):
        bonus_wallet.bet += Decimal('2.00')
        bonus_wallet.save()


def withdrawnbonus(request):
    if request.method == 'POST':
        form = WithdrawnBonusForm(request.user, request.POST)
        if form.is_valid():
            wallet = Wallet.objects.filter(user=request.user)[0]
            wallet_bonus = BonusWallet.objects.filter(user=request.user)[0]
            withdrawn_bonus = form.save(commit=False)
            withdrawn_bonus.accepted = True
            withdrawn_bonus.wallet = wallet
            withdrawn_bonus.save()
            wallet.value += withdrawn_bonus.amount
            wallet_bonus.value -= withdrawn_bonus.amount
            wagering_requirement = WageringRequirement.objects.get().value
            cash_in = wagering_requirement * withdrawn_bonus.amount
            wallet_bonus.bet -= cash_in
            wallet_bonus.save()
            wallet.save()
            return HttpResponse('Withdraw accepted')
        return HttpResponse('You need to play more!!!')

    return HttpResponseRedirect('home')


def withdrawn(request):
    if request.method == 'POST':
        form = WithdrawnMoneyForm(request.user, request.POST)
        if form.is_valid():
            wallet = Wallet.objects.filter(user=request.user)[0]
            withdrawn = form.save(commit=False)
            withdrawn.accepted = True
            withdrawn.wallet = wallet
            withdrawn.save()
            wallet.value -= withdrawn.amount
            wallet.save()
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


class SignupView(FormView):
    template_name = 'igaming/signup.html'
    form_class = SignUpForm
    success_url = '/home'

    def form_valid(self, form):
        form.save()
        return super(SignupView, self).form_valid(form)


def home(request):
    data = {}
    if request.user.is_authenticated:
        data['form'] = MatchForm()
        data['withdrawn_bonus'] = WithdrawnBonusForm(request.user)
        data['withdrawn_money'] = WithdrawnMoneyForm()
        data['deposit'] = DepositForm()
        w = Wallet.objects.filter(user=request.user).aggregate(Sum('value'))
        b = BonusWallet.objects.filter(user=request.user).aggregate(
            Sum('value'), Sum('bet'))
        data['money'] = w['value__sum']
        data['bonus'] = b['value__sum']
        data['wagered'] = b['bet__sum']

    return render(request, 'igaming/home.html', data)
