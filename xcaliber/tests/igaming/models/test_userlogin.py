import pytest
from importlib import import_module

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.sessions.middleware import SessionMiddleware
from django.conf import settings

from igaming.models import UserLogin


@pytest.fixture()
def user(db):
    user = User.objects.create(username='myuser', password='pswd')
    return user


def test_non_user_login_creation(db):
    before = UserLogin.objects.count()
    u = User.objects.create(username="foo")
    u.save()
    after = UserLogin.objects.count()
    assert before == after


def test_user_login_creation(rf, user):
    before = UserLogin.objects.count()

    request = rf.get('/home')
    engine = import_module(settings.SESSION_ENGINE)
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
    request.session = engine.SessionStore(session_key)
    if not request.session.exists(request.session.session_key):
        request.session.create()

    login(request, user)

    after = UserLogin.objects.count()
    assert before < after
