from igaming.forms import DepositForm


def test_deposit_form_invalid_field(user_with_wallet):
    form_data = {'money': 2}
    form = DepositForm(user=user_with_wallet, data=form_data)

    assert not form.is_valid()


def test_deposit_form_valid_field(user_with_wallet):
    form_data = {'value': 2}
    form = DepositForm(user=user_with_wallet, data=form_data)

    assert form.is_valid()
