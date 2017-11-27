import pytest
from decimal import Decimal
from django.contrib.auth.models import User

from igaming.views import decide_match, process_payment
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


@pytest.mark.parametrize("won,expected", [
    (True, Decimal('4.00')),
    (False, Decimal('0.00')),
])
def test_process_payment_nonempty_pocket(db, wallet, won, expected):
    process_payment(wallet, won)

    assert wallet.value == expected
