from django.conf.urls import url

from .views import (PlayView, deposit, home, SignupView, withdrawn,
                    withdrawnbonus)

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^play$', PlayView.as_view(), name='play'),
    url(r'^deposit$', deposit, name='deposit'),
    url(r'^withdrawnbonus$', withdrawnbonus, name='withdrawnbonus'),
    url(r'^withdrawn$', withdrawn, name='withdrawn'),
    url(r'^home$', home, name='home'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
]
