from django.conf.urls import url

from .views import (deposit, home, index, play, signup, withdrawn,
                    withdrawnbonus)

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^play$', play, name='play'),
    url(r'^deposit$', deposit, name='deposit'),
    url(r'^withdrawnbonus$', withdrawnbonus, name='withdrawnbonus'),
    url(r'^withdrawn$', withdrawn, name='withdrawn'),
    url(r'^home$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
]
