import random
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, MatchForm, DepositForm
from .models import Deposit

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.wallet = request.user.wallet
            deposit.save()

    return HttpResponseRedirect('home')


@login_required
def play(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.user = request.user
            match.result = random.randint(0, 36)
            if match.result != match.answer:
                match.won = True
                match.save()
                Deposit.objects.create(wallet=request.user.wallet, value=Decimal('2'))
                return HttpResponseRedirect('home')
            match.save()
            msg = "YOU LOSE!!! Your answer {} is not {}".format(
                match.answer, match.result)
            return HttpResponse(msg)


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
        data['deposit'] = DepositForm()
        data['money'] = request.user.wallet.value

    return render(request, 'igaming/home.html', data)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
