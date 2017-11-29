from importlib import import_module

import pytest
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

from igaming.models import BonusWallet, LoginBonus


@pytest.fixture()
def user(db):
    user = User.objects.create(username='myuser', password='pswd')
    return user


def test_bonus_login_creation(rf, user):
    before_wallet = BonusWallet.objects.count()
    before_bonus = LoginBonus.objects.count()

    request = rf.get('/home')
    engine = import_module(settings.SESSION_ENGINE)
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    request.session = engine.SessionStore(session_key)
    if not request.session.exists(request.session.session_key):
        request.session.create()

    login(request, user)

    after_wallet = BonusWallet.objects.count()
    after_bonus = LoginBonus.objects.count()

    assert before_wallet < after_wallet
    assert before_bonus < after_bonus
