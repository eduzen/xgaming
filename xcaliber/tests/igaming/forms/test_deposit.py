from decimal import Decimal

import pytest
from django.contrib.auth.models import User

from igaming.forms import DepositForm
from igaming.models import Wallet


@pytest.fixture()
def user(db):
    user = User.objects.create(username='myuser', password='pswd')
    wallet = Wallet.objects.create(user=user, value=Decimal('2.00'))
    return user


def test_deposit_form_invalid_field(user):
     form_data = {'money': 2}
     form = DepositForm(user=user, data=form_data)

     assert not form.is_valid()

def test_deposit_form_valid_field(user):
     form_data = {'value': 2}
     form = DepositForm(user=user, data=form_data)

     assert form.is_valid()
