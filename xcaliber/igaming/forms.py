from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from config.models import WageringRequirement

from .models import (BonusWallet, Deposit, Match, Wallet, WithdrawnBonus,
                     WithdrawnMoney)


class WithdrawnMoneyForm(forms.ModelForm):
    class Meta:
        model = WithdrawnMoney
        fields = ('amount', )

    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.user = user
        super(WithdrawnMoneyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'WithdrawnForm'
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = 'withdrawn'

        self.helper.add_input(Submit('submit', 'Submit'))

    def is_valid(self):
        valid = super(WithdrawnMoneyForm, self).is_valid()

        if not valid:
            return valid

        wallet = Wallet.objects.filter(user=self.user)
        if not wallet.exists:
            return False
        wallet = wallet[0]

        if wallet.value < self.cleaned_data['amount']:
            return False

        return True


class WithdrawnBonusForm(forms.ModelForm):
    class Meta:
        model = WithdrawnBonus
        fields = ('amount', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(WithdrawnBonusForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'WithdrawnForm'
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = 'withdrawnbonus'

        self.helper.add_input(Submit('submit', 'Submit'))

    def is_valid(self):
        valid = super(WithdrawnBonusForm, self).is_valid()

        if not valid:
            return valid

        bonus_wallet = BonusWallet.objects.filter(user=self.user)
        if not bonus_wallet.exists:
            return False
        bonus_wallet = bonus_wallet[0]

        wagered = bonus_wallet.bet
        amount_required = self.cleaned_data['amount']
        wagering_requirement = WageringRequirement.objects.get().value

        cash_in = wagering_requirement * amount_required
        if wagered >= cash_in:
            return True

        return False


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'MatchForm'
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = 'play'
        self.helper.layout = Layout(
            Field('answer', ss_class='answer'),
        )

        self.helper.add_input(Submit('submit', 'Submit'))


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        exclude = ('wallet', )

    def __init__(self, user=None, *args, **kwargs):
        if user:
            self.user = user
        super(DepositForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'DepositForm'
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = 'deposit'

        self.helper.add_input(Submit('submit', 'Submit'))

    def is_valid(self):
        valid = super(DepositForm, self).is_valid()

        if not valid:
            return valid

        wallet = Wallet.objects.filter(user=self.user)
        if wallet.exists:
            return True
        return False


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-SignUpForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'

        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2', )
