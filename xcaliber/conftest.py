from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from igaming.models import BonusWallet, Wallet


@pytest.fixture()
def user(db):
    user = User.objects.create(username='myuser', password='pswd')
    return user


@pytest.fixture()
def wallet(db):
    user = User.objects.create(username='myuser', password='pswd')
    wallet = Wallet.objects.create(user=user, value=Decimal('2.00'))
    return wallet


@pytest.fixture()
def user_with_wallet(db):
    user = User.objects.create(username='myuser', password='pswd')
    Wallet.objects.create(user=user, value=Decimal('200.00'))
    return user


@pytest.fixture()
def user_with_bonus_wallet(db):
    user = User.objects.create(username='myuser', password='pswd')
    Wallet.objects.create(user=user, value=Decimal('2.00'))
    bonus_wallet = BonusWallet.objects.create(user=user)
    bonus_wallet.value = 200
    bonus_wallet.bet = 2000
    bonus_wallet.save()
    return user
