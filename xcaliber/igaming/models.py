from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

CURRENCIES = (
    (u'EUR', u'Euro'),
)


class UserLogin(models.Model):
    """Users' logins, one per connection"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = "Users logins"
        verbose_name_plural = "All users logins"


class Wallet(models.Model):
    """
        Wallet for real money for users
    """
    user = models.ForeignKey(User)
    currency = models.CharField(default=CURRENCIES[0][0],
                                max_length=3, choices=CURRENCIES)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = "Real money Wallet"
        verbose_name_plural = "All real money Wallets"


class BonusWallet(models.Model):
    """
        Bonus Wallet for users
    """
    user = models.ForeignKey(User)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)
    bet = models.DecimalField(default=Decimal('0.00'),
                              decimal_places=2, max_digits=13)

    class Meta:
        verbose_name = "Bonus Wallet"
        verbose_name_plural = "All Bonus Wallets"


class Deposit(models.Model):
    """
        It records each real money deposit in a wallet and
        user account. It could be differents currencies for a wallet.
    """
    wallet = models.ForeignKey('Wallet')
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Deposit for user: {}>".format(self.wallet.user.username)

    class Meta:
        verbose_name = "Deposit"
        verbose_name_plural = "All Deposits"


class Bonus(models.Model):
    """ Abstract class for Bonus"""
    wallet = models.ForeignKey('BonusWallet')
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES, default=CURRENCIES[0][0])
    timestamp = models.DateTimeField(auto_now=True)
    wagering_requirement = models.IntegerField(default=10)

    def __str__(self):
        if self.name:
            return self.name
        return 'Bonus'

    class Meta:
        abstract = True


class LoginBonus(Bonus):
    name = models.CharField(max_length=120, default='Login Bonus')
    value = models.DecimalField(default=Decimal('100.00'),
                                max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = "Login Bonus"
        verbose_name_plural = "LoginBonus given"


class DepositBonus(Bonus):
    name = models.CharField(max_length=120, default='Deposit Bonus')
    value = models.DecimalField(default=Decimal('20.00'),
                                max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = "Deposit Bonus"
        verbose_name_plural = "DepositBonus given"


class WithdrawnMoney(models.Model):
    wallet = models.ForeignKey(Wallet)
    timestamp = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    amount = models.DecimalField(default=Decimal('0.00'),
                                 max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = "Withdraw money"
        verbose_name_plural = "Withdraws money"


class WithdrawnBonus(models.Model):
    wallet = models.ForeignKey(Wallet)
    timestamp = models.DateTimeField(auto_now=True)
    accepted = models.BooleanField(default=False)
    amount = models.DecimalField(default=Decimal('0.00'),
                                 max_digits=13, decimal_places=2)

    class Meta:
        verbose_name = "Withdraw bonusmoney"
        verbose_name_plural = "Withdraws bonusmoney"


class Match(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    result = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)
    won = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
