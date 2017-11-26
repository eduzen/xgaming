from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field
from crispy_forms.layout import Layout

from .models import Match, Deposit

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

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'DepositForm'
        self.helper.form_class = ''
        self.helper.form_method = 'post'
        self.helper.form_action = 'deposit'

        self.helper.add_input(Submit('submit', 'Submit'))


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
