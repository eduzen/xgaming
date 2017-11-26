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
    """Users' wallet, one per user"""
    user = models.OneToOneField(User)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)

    def __str__(self):
        return "<Wallet for user: {}>".format(self.user.username)


class Deposit(models.Model):
    """ It could be differents currencies for a wallet """
    wallet = models.ForeignKey('Wallet')
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    value = models.DecimalField(default=Decimal('0.00'),
                                max_digits=13, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Deposit for user: {}>".format(self.wallet.user.username)


class Bonus(models.Model):
    """ Abstract class for Bonus"""
    wallet = models.ForeignKey('Wallet')
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


class WithdrawalRequest(models.Model):
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
    if hasattr(user, 'wallet'):
        bonus = LoginBonus.objects.create(wallet=user.wallet)
        bonus.save()
        user.wallet.value += Decimal(bonus.value)
        user.wallet.save()
    user.save()

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)


@receiver(post_save, sender=Deposit)
def create_deposit_bonus(sender, instance, created, **kwargs):
    if created:
        instance.wallet.value += Decimal(instance.value)
        if instance.value >= Decimal('100.00'):
            d = DepositBonus.objects.create(wallet=instance.wallet)
            instance.wallet.value += Decimal(d.value)
        instance.wallet.save()
