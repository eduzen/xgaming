from decimal import Decimal

import pytest

from igaming.views import Play, deposit, home


@pytest.mark.parametrize("won,expected", [
    (True, Decimal('4.00')),
    (False, Decimal('0.00')),
])
def test_process_payment_nonempty_pocket(db, wallet, won, expected):
    p = Play()
    p._process_payment(wallet, won)

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


def test_deposit_post_view_redirects(rf, wallet, mocker):
    mocker.patch('igaming.views.DepositForm')
    request = rf.post('deposit')
    request.user = wallet.user
    response = deposit(request)
    assert response.status_code == 302
