from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from igaming.models import Wallet


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
    Wallet.objects.create(user=user, value=Decimal('2.00'))
    return user
