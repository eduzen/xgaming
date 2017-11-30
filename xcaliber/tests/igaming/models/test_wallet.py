from django.contrib.auth.models import User
from hypothesis.extra.django.models import models

from igaming.models import Wallet


def test_creation(db):
    wallet = models(Wallet, user=models(User)).example()
    assert wallet
