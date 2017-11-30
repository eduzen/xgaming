from decimal import Decimal

import pytest
from hypothesis import given, strategies as st
from django.core.urlresolvers import reverse

from igaming.views import PlayView, deposit, home

PUBLIC_URLS = ('home', 'signup', 'login', 'logout', 'password_reset')


@given(url_name=st.sampled_from(PUBLIC_URLS))
def test_public_urls(url_name, client):
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200


def test_an_admin_view(admin_client):
    response = admin_client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.parametrize("won,expected", [
    (True, Decimal('4.00')),
    (False, Decimal('0.00')),
])
def test_process_payment_nonempty_pocket(db, wallet, won, expected):
    p = PlayView()
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
