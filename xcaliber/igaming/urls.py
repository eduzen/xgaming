from django.conf.urls import url

from .views import index, home, signup, play
from .views import deposit, withdrawnbonus, withdrawn

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^play$', play, name='play'),
    url(r'^deposit$', deposit, name='deposit'),
    url(r'^withdrawnbonus$', withdrawnbonus, name='withdrawnbonus'),
    url(r'^withdrawn$', withdrawn, name='withdrawn'),
    url(r'^home$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
]
