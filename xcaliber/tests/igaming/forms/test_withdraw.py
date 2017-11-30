from igaming.forms import WithdrawnMoneyForm
from igaming.models import Wallet


def test_invalid_field(user):
    form_data = {'money_money': 2}
    form = WithdrawnMoneyForm(data=form_data)

    assert not form.is_valid()


def test_valid_field_empty_wallet(user):
    form_data = {'amount': 2}
    form = WithdrawnMoneyForm(user, data=form_data)

    assert not form.is_valid()


def test_succes_withdraw(user):
    wallet = Wallet.objects.filter(user=user)[0]
    wallet.value = 50
    wallet.save()
    form_data = {'amount': 3}
    form = WithdrawnMoneyForm(user, data=form_data)

    assert form.is_valid()
