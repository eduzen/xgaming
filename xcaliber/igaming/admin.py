from django.contrib import admin

from .models import (BonusWallet, Deposit, DepositBonus, LoginBonus, UserLogin,
                     Wallet, WithdrawnBonus, WithdrawnMoney)


class DepositInline(admin.TabularInline):
    model = Deposit
    extra = 0


class LoginBonusInline(admin.TabularInline):
    model = LoginBonus
    extra = 0


class DepositBonusInline(admin.TabularInline):
    model = DepositBonus
    extra = 0


class WithdrawnMoneyInline(admin.TabularInline):
    model = WithdrawnMoney
    extra = 0


class WithdrawnBonusInline(admin.TabularInline):
    model = WithdrawnBonus
    extra = 0


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'timestamp', )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'value', 'currency')
    fields = ('user', 'value', 'currency')
    inlines = [
        DepositInline,
        WithdrawnMoneyInline,
        WithdrawnBonusInline,
    ]


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'wallet', 'value', )


@admin.register(LoginBonus)
class LoginBonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', )


@admin.register(DepositBonus)
class DepositBonusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', )


@admin.register(BonusWallet)
class BonusWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'value')
    fields = ('user', 'value')
    inlines = [
        DepositBonusInline,
        LoginBonusInline,
    ]


@admin.register(WithdrawnMoney)
class WithdrawnMoneyAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'timestamp', 'accepted')


@admin.register(WithdrawnBonus)
class WithdrawnBonusAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'timestamp', 'accepted')
