from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from igaming.forms import DepositForm
from igaming.models import Wallet
from igaming.views import decide_match, deposit, home, process_payment


@pytest.fixture()
def user(db):
    user = User.objects.create(username='myuser', password='pswd')
    return user


@pytest.fixture()
def wallet(db):
    user = User.objects.create(username='myuser', password='pswd')
    wallet = Wallet.objects.create(user=user, value=Decimal('2.00'))
    return wallet


@pytest.mark.parametrize("won,expected", [
    (True, Decimal('4.00')),
    (False, Decimal('0.00')),
])
def test_process_payment_nonempty_pocket(db, wallet, won, expected):
    process_payment(wallet, won)

    assert wallet.value == expected

def test_home_view(rf, wallet):
    request = rf.get('home')
    request.user = wallet.user
    response = home(request)
    assert response.status_code == 200


def test_deposit_get_view_redirect(rf, user):
    request = rf.get('deposit')
    request.user = user
    response = deposit(request)
    assert response.status_code == 302


def test_deposit_post_view_redirect(rf, user, mocker):
    request = rf.get('deposit')
    request.user = user
    response = deposit(request)
    assert response.status_code == 302


def test_deposit_post_view_redirect(rf, wallet, mocker):
    mocker.patch('igaming.views.DepositForm')
    request = rf.post('deposit')
    request.user = wallet.user
    response = deposit(request)
    assert response.status_code == 302
