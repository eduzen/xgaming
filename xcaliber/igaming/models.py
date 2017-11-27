from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.utils import timezone


CURRENCIES = (
    (u'EUR', u'Euro'),
    (u'USD', u'US Dollars'),
)


class UserLogin(models.Model):
    """Users' logins, one per connection"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class Wallet(models.Model):
    """
        Wallet for real money for users
    """
    user = models.ForeignKey(User)
    currency = models.CharField(default=CURRENCIES[0][0],
                                max_length=3, choices=CURRENCIES)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)


class BonusWallet(models.Model):
    """
        Bonus Wallet for users
    """
    user = models.ForeignKey(User)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)


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


class Bonus(models.Model):
    """ Abstract class for Bonus"""
    wallet = models.ForeignKey('BonusWallet')
    currency = models.CharField(max_length=3,
                                choices=CURRENCIES, default=CURRENCIES[0][0])
    timestamp = models.DateTimeField(auto_now=True)

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


class DepositBonus(Bonus):
    name = models.CharField(max_length=120, default='Deposit Bonus')
    value = models.DecimalField(default=Decimal('20.00'),
                                max_digits=13, decimal_places=2)


class Withdrawn(models.Model):
    wallet = models.ForeignKey(Wallet)
    timestamp = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(default=Decimal('0.00'),
                                 max_digits=13, decimal_places=2)


class Match(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now=True)
    result = models.IntegerField(null=True, blank=True)
    answer = models.IntegerField(null=True, blank=True)
    won = models.BooleanField(default=False)


# Signals
@receiver(user_logged_in, sender=User)
def update_user_login(sender, user, **kwargs):
    """ It captures each users' login and it creates a new userlogin """
    user.userlogin_set.create(timestamp=timezone.now())
    user.save()

    bonus_wallet = BonusWallet.objects.filter(user=user)
    if not bonus_wallet.exists():
        bonus_wallet = BonusWallet.objects.create(user=user)
        bonus_wallet.save()
    else:
        bonus_wallet = bonus_wallet[0]

    login_bonus = LoginBonus.objects.create(wallet=bonus_wallet)
    bonus_wallet.value += Decimal(login_bonus.value)
    bonus_wallet.save()

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    """
        Every user has an euro wallet
    """
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=Deposit)
def create_deposit_bonus(sender, instance, created, **kwargs):
    """
        We update value preview from wallet and
        every deposit greater than 100 has a bonus
    """
    if created:
        instance.wallet.value += Decimal(instance.value)
        instance.wallet.save()
        if instance.value >= Decimal('100.00'):
            bonus_wallet = BonusWallet.objects.filter(user=instance.wallet.user)
            if not bonus_wallet.exists():
                bonus_wallet = BonusWallet.objects.create(user=instance.wallet.user)
                bonus_wallet.save()
            else:
                bonus_wallet = bonus_wallet[0]

            deposit_bonus = DepositBonus.objects.create(wallet=bonus_wallet)
            bonus_wallet.value += Decimal(deposit_bonus.value)
            bonus_wallet.save()
