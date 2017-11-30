from unittest.mock import MagicMock

from igaming.forms import WithdrawnBonusForm, WithdrawnMoneyForm
from igaming.models import Wallet


def test_invalid_field():
    form_data = {'money_money': 2}
    form = WithdrawnMoneyForm(data=form_data)

    assert not form.is_valid()


def test_bonus_invalid_field():
    form_data = {'money_money': 2}
    form = WithdrawnBonusForm(data=form_data)

    assert not form.is_valid()


def test_valid_field_empty_wallet(user):
    form_data = {'amount': 2}
    form = WithdrawnMoneyForm(user, data=form_data)

    assert not form.is_valid()


def test_bonus_valid_field_empty_wallet(user):
    form_data = {'amount': 2}
    form = WithdrawnMoneyForm(user, data=form_data)

    assert not form.is_valid()


def test_succes_withdraw(user_with_wallet):
    wallet = Wallet.objects.filter(user=user_with_wallet)[0]
    wallet.value = 50
    wallet.save()
    form_data = {'amount': 3}
    form = WithdrawnMoneyForm(user_with_wallet, data=form_data)

    assert form.is_valid()


def test_bonus_succes_withdraw(user_with_bonus_wallet, mocker):
    wagering = mocker.patch(
        'igaming.forms.WageringRequirement.objects.get')
    mock = MagicMock()
    mock.value = 1
    wagering.return_value = mock
    form_data = {'amount': 3}
    form = WithdrawnBonusForm(user_with_bonus_wallet, data=form_data)

    assert form.is_valid()
