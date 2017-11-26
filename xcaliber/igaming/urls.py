from django.conf.urls import url

from .views import index, home, signup, play, deposit

urlpatterns = [
    url(r'^$', home, name='index'),
    url(r'^play$', play, name='play'),
    url(r'^deposit$', deposit, name='deposit'),
    url(r'^home$', home, name='home'),
    url(r'^signup$', signup, name='signup'),
]
