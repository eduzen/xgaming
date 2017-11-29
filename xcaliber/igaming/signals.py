from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import BonusWallet, Deposit, DepositBonus, LoginBonus, Wallet


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
            user = instance.wallet.user
            bonus_wallet = BonusWallet.objects.filter(user=user)
            if not bonus_wallet.exists():
                bonus_wallet = BonusWallet.objects.create(user=user)
                bonus_wallet.save()
            else:
                bonus_wallet = bonus_wallet[0]

            deposit_bonus = DepositBonus.objects.create(wallet=bonus_wallet)
            bonus_wallet.value += Decimal(deposit_bonus.value)
            bonus_wallet.save()
