from collections import defaultdict
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SignUpForm

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
    data = defaultdict()
    if request.user.is_authenticated:
        data['money'] = request.user.wallet.value

    return render(request, 'igaming/home.html', data)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
